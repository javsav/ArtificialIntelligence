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


def get_ordered_path(path_str, start, end):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        curr = path[-1]
        if curr == end:
            return path
        r, c = curr
        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < len(path_str) and 0 <= nc < len(path_str[0]):
                if path_str[nr][nc] == "*" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(path + [(nr, nc)])
    return []


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
    return path, goal


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


def simulated_annealing(path_str, start, end, d):
    ordered_path = get_ordered_path(path_str, start, end)
    i = random.randint(0, len(ordered_path) - 1)
    point_choice = ordered_path[i]

    target_index = min(i + int(d), len(ordered_path) - 1)
    segment_end = ordered_path[target_index]
    return point_choice, segment_end


def calculate_g_cost_of_segment(path_str, start, end, map_int):
    ordered = get_ordered_path(path_str, start, end)
    g_cost = 0
    for i in range(len(ordered) - 1):
        current_node = ordered[i]
        next_path_node = ordered[i + 1]
        cost_difference = map_int[current_node] - map_int[next_path_node]
        g_cost += 1 + max(0, cost_difference)
    return g_cost


def replace_path_segment(
    point_choice, segment_end, old_path_str, map_str, new_segment_str, start, end
):
    old_path_ordered = get_ordered_path(old_path_str, start, end)
    segment_start_index = old_path_ordered.index(point_choice)
    segment_end_index = old_path_ordered.index(segment_end)

    if segment_start_index > segment_end_index:
        segment_start_index, segment_end_index = segment_end_index, segment_start_index

    new_segment_ordered = get_ordered_path(new_segment_str, point_choice, segment_end)
    new_sequence = (
        old_path_ordered[:segment_start_index]
        + new_segment_ordered
        + old_path_ordered[segment_end_index + 1 :]
    )

    new_path_str = copy.deepcopy(map_str)
    for r, c in new_sequence:
        new_path_str[r][c] = "*"

    return new_path_str


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
        point_choice, segment_end = simulated_annealing(path_str, start, end, d)
        path_segment, goal = randomised_breadth_first(
            map, size, point_choice, segment_end, map_str, mode
        )
        new_path_str = replace_path_segment(
            point_choice, segment_end, path_str, map_str, path_segment, start, end
        )
        delta_g = calculate_g_cost_of_segment(
            path_str, start, end, map
        ) - calculate_g_cost_of_segment(new_path_str, start, end, map)
        if delta_g > 0:
            path_str = new_path_str
        else:
            probability = np.exp(float(delta_g) / float(t_ini))
            if random.random() < probability:
                path_str = new_path_str

        path_cost = calculate_g_cost_of_segment(path_str, start, end, map)
        t_cost_list.append((t_ini, path_cost))
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
