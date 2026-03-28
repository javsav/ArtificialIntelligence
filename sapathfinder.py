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
    # if mode == "DEBUG":
    #     print("path:")
    # for i in range(0, size[0], 1):
    #     for j in range(0, size[1], 1):
    #         print(path[i][j], end=" ")
    #     print("\n", end="")

    # print("\n", end="")
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
    path_points = []
    new_end = end
    success = False
    step_x = 1
    if start[0] > end[0]:
        step_x = -1
    step_y = 1
    if start[1] > end[1]:
        step_y = -1
    for i in range(start[0], end[0] + 1, step_x):
        for j in range(start[1], end[1] + 1, step_y):
            if i == start[0] and j == start[1]:
                continue
            if path[i][j] == -2:
                path_points.append((i, j))

    point_choice = random.choice(path_points)
    point_position = None
    for i in range(0, len(path_points)):
        if (path_points)[i] == point_choice:
            point_position = i
    if point_position is None:
        print("Error: could not find point position")
        sys.exit()
    path_points_toward_end = path_points[point_position + 1 :]
    path_points_set = set(path_points_toward_end)
    while path_points_set:
        for i in range(0, len(path_points_toward_end)):
            if manhattan_distance(point_choice, (path_points_toward_end)[i]) == d:
                success = True
                new_end = (path_points_toward_end)[i]
            else:
                success = False
                new_end = end
            path_points_set.remove((path_points_toward_end[i]))
    return success, new_end, point_choice


def calculate_g_cost_of_segment(start, end, map, path):
    g_cost = 0
    step_cost = None
    path_points = []
    step_x = 1
    if start[0] > end[0]:
        step_x = -1
    step_y = 1
    if start[1] > end[1]:
        step_y = -1
    for i in range(start[0], end[0] + 1, step_x):
        for j in range(start[1], end[1] + 1, step_y):
            if path[i][j] == -2:
                path_points.append((i, j))
    path_points_toward_end = path_points
    # print("path")
    # print(path)
    # print(path_points_toward_end)
    # input("...")
    path_points_set = set(path_points_toward_end)
    break_condition = len(path_points_toward_end)
    while path_points_set:
        if len(path_points_set) < break_condition and len(path_points_set) == 1:
            break
        for i in range(0, len(path_points_toward_end) - 1, 1):
            cost_difference = (
                map[path_points_toward_end[i + 1]] - map[path_points_toward_end[i]]
            )
            step_cost = 1 + max(0, cost_difference)
            g_cost += step_cost
            # print("path points to end")
            # print(path_points_toward_end)
            # print("path points set")
            # print(path_points_set)
            # print("path points to end[i]")
            # print((path_points_toward_end[i]))
            # print("i")
            # print(i)
            # input("waiting")
            # if path_points_toward_end[]
            path_points_set.remove((path_points_toward_end[i]))
    return g_cost


def replace_path_segment(
    point_choice, new_end, map, path_segment, path, start, end, size
):

    step_x = 1
    # print("path segment:")
    # print(path_segment)
    # print("original path:")
    # print(path)
    # input("Press Enter")
    new_path = copy.deepcopy(path)
    if point_choice[0] > new_end[0]:
        step_x = -1
    step_y = 1
    if point_choice[1] > new_end[1]:
        step_y = -1
    for i in range(point_choice[0], new_end[0] + 1, step_x):
        for j in range(point_choice[1], new_end[1] + 1, step_y):
            new_path[i][j] = path_segment[i][j]
    new_path_int = np.zeros((size[0], size[1]), dtype=int)
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            if new_path[i][j] == "*":
                new_path_int[i][j] = -2
            elif new_path[i][j] == "X":
                new_path_int[i][j] = -1
            else:
                new_path_int[i][j] = int(new_path[i][j])
    return new_path, new_path_int


def pathfind(mode, map_file, initial_path, t_ini, t_fin, alpha, d):
    size, start, end, map, map_str, path, path_str, t_ini, t_fin, alpha, d = parse_map()
    t_ini = float(t_ini)
    t_fin = float(t_fin)
    alpha = float(alpha)
    d = float(d)
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
    t_cost_list = []
    while t_ini > t_fin:
        success, new_end, point_choice = simulated_annealing(
            path, d, map, size, start, end
        )

        path_segment, num_visits, visit_count, first_visit, last_visit, goal = (
            randomised_breadth_first(map, size, point_choice, new_end, map_str, mode)
        )
        if not goal:
            print("null")
        new_path_str, new_path = replace_path_segment(
            point_choice, new_end, map, path_segment, path_str, start, end, size
        )
        delta_g = calculate_g_cost_of_segment(
            start, end, map, path
        ) - calculate_g_cost_of_segment(start, end, map, new_path)

        if delta_g > 0:
            path = new_path
        else:
            # print("delta-g")
            # print(delta_g)
            # print("t_ini")
            # print(t_ini)
            # print("division")
            # print(float(delta_g) / float(t_ini))
            if delta_g == 0:
                path = new_path
                path_str = new_path_str
            else:
                probability = np.exp(float(delta_g) / float(t_ini))
                if probability > 0.5:
                    path = new_path
                    path_str = new_path_str
        t_cost_list.append(
            (t_ini, calculate_g_cost_of_segment(start, end, map, new_path))
        )
        # print(type(t_ini))
        # print(type(alpha))
        # input("...")
        t_ini = float(alpha * t_ini)
    if mode == "DEBUG":
        print("path:")
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            print(path_str[i][j], end=" ")
        print("\n", end="")
    if mode == "DEBUG":
        print("T&cost:")
        for i in range(0, len(t_cost_list)):
            print(f"T = {t_cost_list[i][0]:.6f}, cost = {t_cost_list[i][1]}")
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
