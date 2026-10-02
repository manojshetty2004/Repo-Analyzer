from google.protobuf.internal import enum_type_wrapper
import argparse

from code_intelligence.bootstrap import build_application


def main():

    parser = argparse.ArgumentParser(
        prog="aise",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    #
    # index
    #

    index = subparsers.add_parser(
        "index",
    )

    index.add_argument(
        "repository",
    )

    #
    # ask
    #

    ask = subparsers.add_parser(
        "ask",
    )

    ask.add_argument(
        "question",
    )

    #
    # analyze
    #

    analyze = subparsers.add_parser(
        "analyze",
    )

    analyze.add_argument(
        "repository",
    )

    architecture = subparsers.add_parser("architecture")
    architecture.add_argument("repository")

    statistics = subparsers.add_parser("stats")
    statistics.add_argument("repository")

    complexity = subparsers.add_parser("complexity")
    complexity.add_argument("repository")

    coupling = subparsers.add_parser("coupling")
    coupling.add_argument("repository")

    dead = subparsers.add_parser("dead-code")
    dead.add_argument("repository")

    duplicates = subparsers.add_parser("duplicates")
    duplicates.add_argument("repository")

    circular = subparsers.add_parser("circular")
    circular.add_argument("repository")

    args = parser.parse_args()

    app = build_application()

    if args.command == "index":

        app.index(
            args.repository,
        )

    elif args.command == "ask":

        print(app.ask(
            args.question,
        ))

    elif args.command == "analyze":

        report = app.analyze(
            args.repository,
        )

        print(report.model_dump_json(indent=2))
        
    elif args.command == "architecture":
        app.architecture(args.repository)

    elif args.command == "stats":
        app.statistics(args.repository)

    elif args.command == "complexity":
        app.complexity(args.repository)

    elif args.command == "coupling":
        app.coupling(args.repository)

    elif args.command == "dead-code":
        app.dead_code(args.repository)

    elif args.command == "duplicates":
        app.duplicates(args.repository)

    elif args.command == "circular":
        app.circular(args.repository)


if __name__ == "__main__":
    main()