import copy
import sys
from collections import deque

import numpy as np

visit_count = 0

if len(sys.argv) < 4:
    print("too few arguments")
    sys.exit(1)
elif len(sys.argv) < 5:
    sys.argv.append("euclidian")


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


def add_surrounding_nodes_to_fringe(
    map, position, fringe, size, visited, previous_node_map
):
    # check above
    if (
        (position[0] - 1) > -1
        and map[position[0] - 1][position[1]]
        and not visited[position[0] - 1][position[1]]
    ):
        fringe.appendleft((position[0] - 1, position[1]))
        if not previous_node_map[(position[0] - 1, position[1])]:
            previous_node_map[(position[0] - 1, position[1])] = position

    # check below
    if (
        (position[0] + 1) < size[0]
        and map[position[0] + 1][position[1]]
        and not visited[position[0] + 1][position[1]]
    ):
        fringe.appendleft((position[0] + 1, position[1]))
        if not previous_node_map[(position[0] + 1, position[1])]:
            previous_node_map[(position[0] + 1, position[1])] = position

    # check to left
    if (
        (position[1] - 1) > -1
        and map[position[0]][position[1] - 1]
        and not visited[position[0]][position[1] - 1]
    ):
        fringe.appendleft((position[0], position[1] - 1))
        if not previous_node_map[(position[0], position[1 - 1])]:
            previous_node_map[(position[0], position[1] - 1)] = position

    # check to right
    if (
        (position[1] + 1) < size[1]
        and map[position[0]][position[1] + 1]
        and not visited[position[0]][position[1] + 1]
    ):
        fringe.appendleft((position[0], position[1] + 1))
        if not previous_node_map[(position[0], position[1 + 1])]:
            previous_node_map[(position[0], position[1] + 1)] = position


def breadth_first(map, size, start, end, map_original):
    to_visit = deque()
    to_visit.appendleft(start)
    visited = np.ones((size[0], size[1]), dtype=bool)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            visited[i][j] = False

    visit_num = np.zeros((size[0], size[1]), dtype=int)

    first_visit = np.zeros((size[0], size[1]), dtype=int)
    last_visit = np.zeros((size[0], size[1]), dtype=int)

    path = copy.deepcopy(map_original)

    closed = np.ones((size[0], size[1]), dtype=bool)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            closed[i][j] = False
    previous_node_map = {}
    while to_visit:
        global visit_count
        current_node = to_visit.pop()
        last_visit[current_node] = visit_count
        visit_num[current_node] += 1
        if visited[current_node]:
            continue
        visited[current_node] = True
        add_surrounding_nodes_to_fringe(
            map, current_node, to_visit, size, visited, previous_node_map
        )
        visit_count = visit_count + 1
        if not first_visit[current_node]:
            first_visit[current_node] = visit_count
        if current_node == end:
            break
    path[end[0]][end[1]] = "*"
    while end != start:
        x = previous_node_map[end][0]
        y = previous_node_map[end][1]
        path[x][y] = "*"
        end = previous_node_map[end]
    path[start[0]][start[1]] = "*"
    print("path:")
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            print(path[i][j], end=" ")
        print("\n", end="")
    return path, visit_num, visit_count, first_visit, last_visit


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
    start = (int(start_string_split[0]) - 1, int(start_string_split[1]) - 1)

    end_string_split = end_string.split()
    if len(end_string_split) < 2:
        print("Error:, end position must have 2 coordinates")
        sys.exit()
    end = (int(end_string_split[0]) - 1, int(end_string_split[1]) - 1)

    remaining_lines = lines[3:]
    map_array = [line.split() for line in remaining_lines]
    map_array_int = np.zeros((size[0], size[1]), dtype=int)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            if map_array[i][j] == "X":
                map_array_int[i][j] = 0
            else:
                map_array_int[i][j] = int(map_array[i][j])

    return size, start, end, map_array_int, map_array


def pathfind(mode, map_file, algorithm, heuristic="euclidian"):
    size, start, end, map, map_str = parse_map()
    if algorithm == "BFS":
        path, visit_num, visit_count, first_visit, last_visit = breadth_first(
            map, size, start, end, map_str
        )
        if mode == "DEBUG":
            visit_size = len(str(abs(visit_count)))
            print("#visits:")
            for i in range(0, size[0], 1):
                for j in range(0, size[1], 1):
                    print(f"{visit_num[i][j]:{visit_size}d}", end=" ")
                print("\n", end="")
            print("first visit:")
            for i in range(0, size[0], 1):
                for j in range(0, size[1], 1):
                    print(f"{first_visit[i][j]:{visit_size}d}", end=" ")
                print("\n", end="")
            print("last visit:")
            for i in range(0, size[0], 1):
                for j in range(0, size[1], 1):
                    print(f"{last_visit[i][j]:{visit_size}d}", end=" ")
                print("\n", end="")
    elif algorithm == "UCS":
        print("Not yet implemented")
        sys.exit()
    elif algorithm == "A*":
        print("Not yet implemented")
        sys.exit()
    else:
        print("Valid algorithms are BFS, UCS or A* (case insensitive)")
        sys.exit()


parse_mode(sys.argv[1].upper(), sys.argv[2], sys.argv[3].upper(), sys.argv[4].upper())
