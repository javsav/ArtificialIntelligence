import sys
from collections import deque

import numpy as np

visit_count = 0

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


def add_surrounding_nodes_to_deque(map, position, deque, size, visited):
    # check above
    if (
        (position[0] - 1) > -1
        and map[position[0] - 1][position[1]]
        and not visited[position[0] - 1][position[1]]
    ):
        deque.appendleft((position[0] - 1, position[1]))

    # check below
    if (
        (position[0] + 1) < size[0]
        and map[position[0] + 1][position[1]]
        and not visited[position[0] + 1][position[1]]
    ):
        deque.appendleft((position[0] + 1, position[1]))

    # check to left
    if (
        (position[1] - 1) > -1
        and map[position[0]][position[1] - 1]
        and not visited[position[0]][position[1] - 1]
    ):
        deque.appendleft((position[0], position[1] - 1))

    # check to right
    if (
        (position[1] + 1) < size[1]
        and map[position[0]][position[1] + 1]
        and not visited[position[0]][position[1] + 1]
    ):
        deque.appendleft((position[0], position[1] + 1))


def breadth_first(map, size, start, end):
    to_visit = deque()
    to_visit.appendleft(start)
    visited = np.ones((size[0], size[1]), dtype=bool)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            visited[i][j] = False

    closed = np.ones((size[0], size[1]), dtype=bool)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            closed[i][j] = False

    while to_visit:
        current_node = to_visit.pop()
        add_surrounding_nodes_to_deque(map, current_node, to_visit, size, visited)
    temp_visit_count = visit_count
    visit_count = 0
    return temp_visit_count


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
    size = (int(size_string_split[0]), int(size_string_split[1]))

    start_string_split = start_string.split()
    if len(start_string_split) < 2:
        print("Error:, start position must have 2 coordinates")
        sys.exit()
    start = (int(start_string_split[0]), int(start_string_split[1]))

    end_string_split = end_string.split()
    if len(end_string_split) < 2:
        print("Error:, end position must have 2 coordinates")
        sys.exit()
    end = (int(end_string_split[0]), int(end_string_split[1]))

    remaining_lines = lines[3:]
    map_array = [line.split() for line in remaining_lines]
    map_array_int = np.zeros((size[0], size[1]), dtype=int)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            if map_array[i][j] == "X":
                map_array_int[i][j] = 0
            else:
                map_array_int[i][j] = int(map_array[i][j])

    return size, start, end, map_array_int


def pathfind(mode, map_file, algorithm, heuristic="euclidian"):
    if mode == "DEBUG":
        print("debug mode")
        size, start, end, map = parse_map()
        print(map)
        breadth_first(map, size, start, end)
    else:
        size, start, end, map = parse_map()


parse_mode(sys.argv[1].upper(), sys.argv[2], sys.argv[3].upper(), sys.argv[4].upper())
