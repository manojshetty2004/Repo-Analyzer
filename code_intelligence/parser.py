from pathlib import Path
import ast
import re
from code_intelligence.models import (
    ModuleInfo,
    ImportInfo,
    ClassInfo,
    FunctionInfo,
)
from code_intelligence.visitor import PythonVisitor


class PythonParser:

    def parse(self, file_path: Path) -> ModuleInfo:
        source = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
        tree = ast.parse(source)
        visitor = PythonVisitor(file_path)
        visitor.visit(tree)

        # Populate source code fields
        lines = source.splitlines()
        for cls in visitor.module.classes:
            if cls.start_line is not None and cls.end_line is not None:
                cls_lines = lines[cls.start_line - 1 : cls.end_line]
                cls.source_code = "\n".join(cls_lines)
            for method in cls.methods:
                if method.start_line is not None and method.end_line is not None:
                    method_lines = lines[method.start_line - 1 : method.end_line]
                    method.source_code = "\n".join(method_lines)
            
        for func in visitor.module.functions:
            if func.start_line is not None and func.end_line is not None:
                func_lines = lines[func.start_line - 1 : func.end_line]
                func.source_code = "\n".join(func_lines)

        return visitor.module


class JSParser:

    def parse(self, file_path: Path) -> ModuleInfo:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = source.splitlines()

        imports = []
        classes = []
        functions = []

        # 1. Parse Imports
        es6_pattern = re.compile(r'import\s+(?:[^"\']+\s+from\s+)?["\']([^"\']+)["\']')
        cjs_pattern = re.compile(r'(?:const|let|var)?\s*(?:[^=]+=\s*)?require\s*\(\s*["\']([^"\']+)["\']\s*\)')

        for line in lines:
            clean_line = re.sub(r'//.*', '', line).strip()
            m = es6_pattern.search(clean_line)
            if m:
                imports.append(ImportInfo(module=m.group(1)))
                continue
            m = cjs_pattern.search(clean_line)
            if m:
                imports.append(ImportInfo(module=m.group(1)))

        # 2. Parse Classes and Functions line-by-line
        brace_depth = 0
        active_class = None
        class_brace_start = 0

        active_func = None
        func_brace_start = 0

        for idx, line in enumerate(lines):
            line_num = idx + 1

            clean_line = re.sub(r'"[^"]*"|\'[^\']*\'|`[^`]*`', '', line)
            clean_line = re.sub(r'//.*', '', clean_line)

            opens = clean_line.count('{')
            closes = clean_line.count('}')

            if active_class is None:
                class_match = re.search(
                    r'\bclass\s+([a-zA-Z0-9_$]+)(?:\s+extends\s+([a-zA-Z0-9_$]+))?',
                    line
                )
                if class_match:
                    name = class_match.group(1)
                    base_classes = [class_match.group(2)] if class_match.group(2) else []
                    active_class = ClassInfo(
                        name=name,
                        qualified_name=name,
                        base_classes=base_classes,
                        start_line=line_num,
                        end_line=line_num
                    )
                    class_brace_start = brace_depth

            if active_func is None:
                func_decl = re.search(r'\bfunction\s+([a-zA-Z0-9_$]+)\s*\(', line)
                arrow_func = re.search(
                    r'\b(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>',
                    line
                )
                async_func = re.search(r'\basync\s+function\s+([a-zA-Z0-9_$]+)\s*\(', line)

                func_match = func_decl or arrow_func or async_func

                method_match = None
                if active_class is not None and brace_depth == class_brace_start + 1:
                    method_search = re.search(
                        r'^\s*(?:async\s+)?([a-zA-Z0-9_$]+)\s*\([^)]*\)\s*\{?',
                        line
                    )
                    if method_search:
                        m_name = method_search.group(1)
                        if m_name not in ('if', 'for', 'while', 'switch', 'catch', 'function', 'class'):
                            method_match = method_search

                if func_match:
                    name = func_match.group(1)
                    active_func = FunctionInfo(
                        name=name,
                        qualified_name=f"{active_class.name}.{name}" if active_class else name,
                        start_line=line_num,
                        end_line=line_num
                    )
                    func_brace_start = brace_depth
                elif method_match:
                    name = method_match.group(1)
                    active_func = FunctionInfo(
                        name=name,
                        qualified_name=f"{active_class.name}.{name}",
                        start_line=line_num,
                        end_line=line_num
                    )
                    func_brace_start = brace_depth

            brace_depth += opens
            brace_depth -= closes

            if active_func is not None:
                if brace_depth <= func_brace_start:
                    active_func.end_line = line_num
                    func_lines = lines[active_func.start_line - 1 : active_func.end_line]
                    active_func.source_code = "\n".join(func_lines)

                    if active_class is not None:
                        active_class.methods.append(active_func)
                    else:
                        functions.append(active_func)
                    active_func = None

            if active_class is not None:
                if brace_depth <= class_brace_start:
                    active_class.end_line = line_num
                    class_lines = lines[active_class.start_line - 1 : active_class.end_line]
                    active_class.source_code = "\n".join(class_lines)

                    classes.append(active_class)
                    active_class = None

        return ModuleInfo(
            path=file_path,
            imports=imports,
            classes=classes,
            functions=functions
        )