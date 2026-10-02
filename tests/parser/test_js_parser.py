from pathlib import Path
from code_intelligence.parser import JSParser


def test_js_parser_imports_and_symbols(tmp_path):
    code = """
import { useState } from 'react';
import defaultExport from "react-dom";
const fs = require('fs');
require("path");

class MyJSClass {
    constructor() {
        this.value = 10;
    }
    
    async myMethod(x) {
        return x + this.value;
    }
}

function globalFunc(a, b) {
    return a + b;
}

const arrowFunc = (val) => {
    console.log(val);
}
"""
    file_path = tmp_path / "test_module.ts"
    file_path.write_text(code, encoding="utf-8")

    parser = JSParser()
    module = parser.parse(file_path)

    # Verify path
    assert module.path == file_path

    # Verify imports
    assert len(module.imports) == 4
    modules_imported = [imp.module for imp in module.imports]
    assert "react" in modules_imported
    assert "react-dom" in modules_imported
    assert "fs" in modules_imported
    assert "path" in modules_imported

    # Verify classes
    assert len(module.classes) == 1
    cls = module.classes[0]
    assert cls.name == "MyJSClass"
    assert cls.start_line == 7
    assert cls.end_line == 15
    assert "class MyJSClass {" in cls.source_code

    # Verify class methods
    assert len(cls.methods) == 2
    
    m_constructor = cls.methods[0]
    assert m_constructor.name == "constructor"
    assert m_constructor.qualified_name == "MyJSClass.constructor"
    assert m_constructor.start_line == 8
    assert m_constructor.end_line == 10
    
    method = cls.methods[1]
    assert method.name == "myMethod"
    assert method.qualified_name == "MyJSClass.myMethod"
    assert method.start_line == 12
    assert method.end_line == 14
    assert "async myMethod(x) {" in method.source_code

    # Verify functions
    assert len(module.functions) == 2
    func1 = module.functions[0]
    assert func1.name == "globalFunc"
    assert func1.start_line == 17
    assert func1.end_line == 19
    assert "function globalFunc(a, b)" in func1.source_code

    func2 = module.functions[1]
    assert func2.name == "arrowFunc"
    assert func2.start_line == 21
    assert func2.end_line == 23
    assert "const arrowFunc = (val) =>" in func2.source_code
