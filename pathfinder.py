import sys


def print_uppercase(s):
    print(f"uppercase: {s.upper()}")


if len(sys.argv) < 5:
    print("too few arguments")
    sys.exit(1)


def parse_mode(arg1):
    match arg1:
        case "DEBUG":
            pathfind(1, 2)
        case "RELEASE":
            pathfind(2, 2)
        case _:
            return (
                "Invalid argument - please pass debug or release as the first command"
            )


def pathfind(mode, map):
    print(mode)


parse_mode(sys.argv[1].upper())
