import sys

import numpy

if len(sys.argv) < 5:
    print("too few arguments")
    sys.exit(1)


def parse_mode(arg1, arg2, arg3, arg4):
    match arg1:
        case "DEBUG":
            pathfind(arg1, arg2, arg3, arg4)
        case "RELEASE":
            pathfind(arg1, arg2, arg3, arg4)
        case _:
            return print(
                "Invalid argument - please pass debug or release as the first command"
            )


map_string = """ """


def parse_map():
    try:
        with open(sys.argv[2], "r") as file:
            map_string = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{sys.argv[2]}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print(map_string)


def pathfind(mode, map, algorithm, heuristic="euclidian"):
    if mode == "DEBUG":
        print("debug mode")
        parse_map()
    else:
        parse_map()


parse_mode(sys.argv[1].upper(), sys.argv[2], sys.argv[3].upper(), sys.argv[4].upper())
