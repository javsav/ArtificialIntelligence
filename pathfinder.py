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


def parse_map():
    map_string = """ """
    try:
        with open(sys.argv[2], "r") as file:
            map_string = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{sys.argv[2]}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    lines = map_string.splitlines()
    size_string, start_string, end_string = lines[:3]

    size_string_split = size_string.split()
    if len(size_string_split) < 2:
        print("Error:, map size must have 2 coordinates")
        sys.exit()
    size = (size_string_split[0], size_string_split[1])

    start_string_split = start_string.split()
    if len(start_string_split) < 2:
        print("Error:, start position must have 2 coordinates")
        sys.exit()
    start = (start_string_split[0], start_string_split[1])

    end_string_split = end_string.split()
    if len(end_string_split) < 2:
        print("Error:, end position must have 2 coordinates")
        sys.exit()
    end = (end_string_split[0], end_string_split[1])

    remaining_lines = lines[3:]
    map_array = [line.split() for line in remaining_lines]
    return size, start, end, map_array


def pathfind(mode, map, algorithm, heuristic="euclidian"):
    if mode == "DEBUG":
        print("debug mode")
        parse_map()
    else:
        parse_map()


parse_mode(sys.argv[1].upper(), sys.argv[2], sys.argv[3].upper(), sys.argv[4].upper())
