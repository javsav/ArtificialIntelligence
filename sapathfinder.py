import copy
import heapq
import random
import sys
from collections import deque

import numpy as np

visit_count = 0
invalid = -1
if len(sys.argv) < 8:
    print("too few arguments")
    sys.exit(1)


def parse_mode(arg1, arg2, arg3, arg4, arg5, arg6, arg7):
    match arg1:
        case "DEBUG":
            pathfind(arg1, arg2, arg3, arg4, arg5, arg6, arg7)
        case "RELEASE":
            pathfind(arg1, arg2, arg3, arg4, arg5, arg6, arg7)
        case _:
            return print(
                "Invalid argument - please pass debug or release as the first command"
            )


def add_surrounding_nodes_to_fringe(
    map, position, fringe, size, visited, previous_node_map, algorithm
):
    global visit_count, invalid
    possible_directions = {0, 1, 2, 3}
    while possible_directions:
        direction = random.choice(tuple(possible_directions))
        possible_directions.remove(direction)
        if direction == 0:
            # check above
            adjacent_node = (position[0] - 1, position[1])
            if (
                adjacent_node[0] > -1 and map[adjacent_node] != invalid
                # and not visited[position[0] - 1][position[1]]
            ):
                fringe.appendleft(adjacent_node)
                if (adjacent_node) not in previous_node_map:
                    previous_node_map[adjacent_node] = position

        elif direction == 1:
            # check below
            adjacent_node = (position[0] + 1, position[1])
            if (
                adjacent_node[0] < size[0] and map[adjacent_node] != invalid
                # and not visited[position[0] + 1][position[1]]
            ):
                fringe.appendleft(adjacent_node)
                if (adjacent_node) not in previous_node_map:
                    previous_node_map[adjacent_node] = position

        elif direction == 2:
            # check to left
            adjacent_node = (position[0], position[1] - 1)
            if (
                (adjacent_node[1]) > -1 and map[adjacent_node] != invalid
                # and not visited[position[0]][position[1] - 1]
            ):
                fringe.appendleft(adjacent_node)
                if (adjacent_node) not in previous_node_map:
                    previous_node_map[adjacent_node] = position

        elif direction == 3:
            # check to right
            adjacent_node = (position[0], position[1] + 1)
            if (
                (adjacent_node[1]) < size[1] and map[adjacent_node] != invalid
                # and not visited[position[0]][position[1] + 1]
            ):
                fringe.appendleft(adjacent_node)
                if (adjacent_node) not in previous_node_map:
                    previous_node_map[adjacent_node] = position


def randomised_breadth_first(map, size, start, end, map_original, mode):
    goal = None
    to_visit = deque()
    to_visit.appendleft(start)
    visited = np.ones((size[0], size[1]), dtype=bool)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            visited[i][j] = False

    num_visits = np.zeros((size[0], size[1]), dtype=int)

    first_visit = np.zeros((size[0], size[1]), dtype=int)
    last_visit = np.zeros((size[0], size[1]), dtype=int)

    path = copy.deepcopy(map_original)

    previous_node_map = {}
    while to_visit:
        global visit_count
        visit_count = visit_count + 1
        current_node = to_visit.pop()
        last_visit[current_node] = visit_count
        num_visits[current_node] += 1
        if visited[current_node]:
            continue
        visited[current_node] = True
        add_surrounding_nodes_to_fringe(
            map, current_node, to_visit, size, visited, previous_node_map, "BFS"
        )

        if not first_visit[current_node]:
            first_visit[current_node] = visit_count
        if current_node == end:
            goal = True
            break
    if current_node != end:
        goal = False
        return path, num_visits, visit_count, first_visit, last_visit, goal
    path[end[0]][end[1]] = "*"
    while end != start:
        x = previous_node_map[end][0]
        y = previous_node_map[end][1]
        path[x][y] = "*"
        end = previous_node_map[end]
    path[start[0]][start[1]] = "*"
    if mode == "DEBUG":
        print("path:")
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            print(path[i][j], end=" ")
        print("\n", end="")
    return path, num_visits, visit_count, first_visit, last_visit, goal


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
    if len(size_string_split) != 2:
        print("Error:, map size must have 2 coordinates")
        sys.exit()
    size = (int(size_string_split[0]), int(size_string_split[1]))

    start_string_split = start_string.split()
    if len(start_string_split) != 2:
        print("Error:, start position must have 2 coordinates")
        sys.exit()
    start = (int(start_string_split[0]) - 1, int(start_string_split[1]) - 1)

    end_string_split = end_string.split()
    if len(end_string_split) != 2:
        print("Error:, end position must have 2 coordinates")
        sys.exit()
    end = (int(end_string_split[0]) - 1, int(end_string_split[1]) - 1)

    map_lines = lines[3:]
    map_array = [line.split() for line in map_lines]
    map_array_int = np.zeros((size[0], size[1]), dtype=int)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            if map_array[i][j] == "X":
                map_array_int[i][j] = -1
            else:
                map_array_int[i][j] = int(map_array[i][j])

    path_string = """ """
    try:
        with open(sys.argv[3], "r") as file:
            path_string = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{sys.argv[3]}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    lines = path_string.splitlines()
    path_lines = lines[0:]
    path_array = [line.split() for line in path_lines]
    path_array_int = np.zeros((size[0], size[1]), dtype=int)
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            if path_array[i][j] == "X":
                path_array_int[i][j] = -1
            elif path_array[i][j] == "*":
                path_array_int[i][j] = -2
            else:
                path_array_int[i][j] = int(path_array[i][j])

    t_ini = sys.argv[4]
    t_fin = sys.argv[5]
    alpha = sys.argv[6]
    d = sys.argv[7]

    return (
        size,
        start,
        end,
        map_array_int,
        map_array,
        path_array_int,
        path_array,
        t_ini,
        t_fin,
        alpha,
        d,
    )


def manhattan_distance(pos1, pos2):
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


def simulated_annealing(path, d, map, size, start, end):
    path_points = {(start)}
    success = False
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            if i == start[0] and j == start[1]:
                continue
            if path[i][j] == -2:
                path_points.add((i, j))

    point_choice = random.choice(tuple(path_points))
    point_position = 0
    for i in range(0, len(tuple(path_points))):
        if tuple(path_points)[i] == point_choice:
            point_position = i
    path_points_list = tuple(path_points)
    path_points_toward_end = path_points_list[point_position:]
    path_points_set = set(path_points_toward_end)
    while path_points_set:
        for i in range(0, len(tuple(path_points_set))):
            if manhattan_distance(point_choice, tuple(path_points)[i]) == d:
                success = True
                new_end = tuple(path_points)[i]
            else:
                success = False
                new_end = end
        path_points_set.remove(tuple(path_points)[i])
    return success, new_end, point_choice


def pathfind(mode, map_file, initial_path, t_ini, t_fin, alpha, d):
    size, start, end, map, map_str, path, path_str, t_ini, t_fin, alpha, d = parse_map()
    # print(
    #     f"size:{size}, start:{start}, end:{end}, t_ini:{t_ini}, t_fin:{t_fin}, alpha:{alpha}, d:{d}"
    # )
    # print("map")
    # print(map)
    # print("path")
    # print(path)
    # print("path_str")
    # print(path_str)
    # input("Press enter to continue")
    while t_ini > t_fin:
        success, new_end, point_choice = simulated_annealing(
            path, d, map, size, start, end
        )

        path, num_visits, visit_count, first_visit, last_visit, goal, cost = (
            randomised_breadth_first(map, size, point_choice, new_end, map_str, mode)
        )
        if not goal:
            print("null")
        t_ini = alpha * t_ini
    if mode == "DEBUG":
        x_string = "X"
        dot_string = "."
        visit_size = len(str(abs(visit_count)))
        print("#visits:")
        max_num_visits = 0
        for i in range(0, size[0], 1):
            for j in range(0, size[1], 1):
                if num_visits[i][j] > max_num_visits:
                    max_num_visits = num_visits[i][j]
        max_num_visits_digits = 0
        while max_num_visits > 0:
            max_num_visits //= 10
            max_num_visits_digits += 1

        for i in range(0, size[0], 1):
            for j in range(0, size[1], 1):
                if num_visits[i][j] == 0 and map_str[i][j] == "X":
                    print(f"{x_string:{max_num_visits_digits}s}", end=" ")
                elif num_visits[i][j] == 0 and map_str[i][j] != "X":
                    print(f"{dot_string:{max_num_visits_digits}s}", end=" ")
                else:
                    print(f"{num_visits[i][j]:{max_num_visits_digits}d}", end=" ")
            print("\n", end="")
        print("first visit:")
        for i in range(0, size[0], 1):
            for j in range(0, size[1], 1):
                if first_visit[i][j] == 0 and map_str[i][j] == "X":
                    print(f"{x_string:{visit_size}s}", end=" ")
                else:
                    print(f"{first_visit[i][j]:{visit_size}d}", end=" ")
            print("\n", end="")
        print("last visit:")
        for i in range(0, size[0], 1):
            for j in range(0, size[1], 1):
                if last_visit[i][j] == 0 and map_str[i][j] == "X":
                    print(f"{x_string:{visit_size}s}", end=" ")
                else:
                    print(f"{last_visit[i][j]:{visit_size}d}", end=" ")
            print("\n", end="")


parse_mode(
    sys.argv[1].upper(),
    sys.argv[2],
    sys.argv[3],
    sys.argv[4],
    sys.argv[5],
    sys.argv[6],
    sys.argv[7],
)
