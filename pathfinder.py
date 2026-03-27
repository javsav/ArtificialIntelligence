import copy
import heapq
import sys
from collections import deque

import numpy as np

visit_count = 0
invalid = -1
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
    map, position, fringe, size, visited, previous_node_map, algorithm
):
    global visit_count, invalid
    # check above
    adjacent_node = (position[0] - 1, position[1])
    if (
        adjacent_node[0] > -1 and map[adjacent_node] != invalid
        # and not visited[position[0] - 1][position[1]]
    ):
        if algorithm == "BFS":
            fringe.appendleft(adjacent_node)
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position
        elif algorithm == "UCS":
            heapq.heappush(fringe, (map[adjacent_node], adjacent_node))
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position

    # check below
    adjacent_node = (position[0] + 1, position[1])
    if (
        adjacent_node[0] < size[0] and map[adjacent_node] != invalid
        # and not visited[position[0] + 1][position[1]]
    ):
        if algorithm == "BFS":
            fringe.appendleft(adjacent_node)
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position
        elif algorithm == "UCS":
            heapq.heappush(fringe, (map[adjacent_node], adjacent_node))
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position

    # check to left
    adjacent_node = (position[0], position[1] - 1)
    if (
        (adjacent_node[1]) > -1 and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] - 1]
    ):
        if algorithm == "BFS":
            fringe.appendleft(adjacent_node)
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position
        elif algorithm == "UCS":
            heapq.heappush(fringe, (map[adjacent_node], adjacent_node))
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position

    # check to right
    adjacent_node = (position[0], position[1] + 1)
    if (
        (adjacent_node[1]) < size[1] and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] + 1]
    ):
        if algorithm == "BFS":
            fringe.appendleft(adjacent_node)
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position
        elif algorithm == "UCS":
            heapq.heappush(fringe, (map[adjacent_node], adjacent_node))
            if (adjacent_node) not in previous_node_map:
                previous_node_map[adjacent_node] = position


def breadth_first(map, size, start, end, map_original, mode):
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


tie_breaker = 0


def add_surrounding_nodes_to_fringe_ucs(
    map, current_node, fringe, size, visited, previous_node_map, cost
):
    global tie_breaker, invalid, visit_count
    position = current_node

    # check above
    adjacent_node = (position[0] - 1, position[1])
    if (
        adjacent_node[0] > -1 and map[adjacent_node] != invalid
        # and not visited[position[0] - 1][position[1]]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        heapq.heappush(fringe, (path_cost, tie_breaker, adjacent_node))
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (path_cost, position)

    # check below
    adjacent_node = (position[0] + 1, position[1])
    if (
        adjacent_node[0] < size[0] and map[adjacent_node] != invalid
        # and not visited[position[0] + 1][position[1]]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        heapq.heappush(fringe, (path_cost, tie_breaker, adjacent_node))
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (path_cost, position)

    # check to left
    adjacent_node = (position[0], position[1] - 1)
    if (
        (adjacent_node[1]) > -1 and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] - 1]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        heapq.heappush(fringe, (path_cost, tie_breaker, adjacent_node))
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (path_cost, position)

    # check to right
    adjacent_node = (position[0], position[1] + 1)
    if (
        (adjacent_node[1]) < size[1] and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] + 1]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        heapq.heappush(fringe, (path_cost, tie_breaker, adjacent_node))
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (path_cost, position)


def uniform_cost(map, size, start, end, map_original, mode):
    goal = None
    global tie_breaker
    tie_breaker = 0
    to_visit = [(0, tie_breaker, start)]
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
        cost, _, current_node = heapq.heappop(to_visit)
        last_visit[current_node] = visit_count
        num_visits[current_node] += 1
        if visited[current_node]:
            continue
        visited[current_node] = True
        add_surrounding_nodes_to_fringe_ucs(
            map,
            current_node,
            to_visit,
            size,
            visited,
            previous_node_map,
            cost,
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
        cost = previous_node_map[end][0]
        x = previous_node_map[end][1][0]
        y = previous_node_map[end][1][1]
        path[x][y] = "*"
        end = previous_node_map[end][1]
    path[start[0]][start[1]] = "*"
    if mode == "DEBUG":
        print("path:")
    for i in range(0, size[0], 1):
        for j in range(0, size[1], 1):
            print(path[i][j], end=" ")
        print("\n", end="")
    return path, num_visits, visit_count, first_visit, last_visit, goal


def euclidian_distance(pos1, pos2):
    x = pos2[0] - pos1[0]
    y = pos2[1] - pos1[1]
    return np.sqrt(x * x + y * y)


def manhattan_distance(pos1, pos2):
    x1 = pos1[0]
    x2 = pos2[0]
    y1 = pos1[1]
    y2 = pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


def add_surrounding_nodes_to_fringe_astar(
    map, current_node, fringe, size, visited, previous_node_map, cost, heuristic, end
):
    global tie_breaker, invalid, visit_count
    position = current_node

    # check above
    adjacent_node = (position[0] - 1, position[1])
    if (
        adjacent_node[0] > -1 and map[adjacent_node] != invalid
        # and not visited[position[0] - 1][position[1]]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        if heuristic == "EUCLIDIAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )

        elif heuristic == "MANHATTAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (
                path_cost,
                position,
            )

    # check below
    adjacent_node = (position[0] + 1, position[1])
    if (
        adjacent_node[0] < size[0] and map[adjacent_node] != invalid
        # and not visited[position[0] + 1][position[1]]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        if heuristic == "EUCLIDIAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )

        elif heuristic == "MANHATTAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (
                path_cost,
                position,
            )

    # check to left
    adjacent_node = (position[0], position[1] - 1)
    if (
        (adjacent_node[1]) > -1 and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] - 1]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        if heuristic == "EUCLIDIAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )

        elif heuristic == "MANHATTAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (
                path_cost,
                position,
            )

    # check to right
    adjacent_node = (position[0], position[1] + 1)
    if (
        (adjacent_node[1]) < size[1] and map[adjacent_node] != invalid
        # and not visited[position[0]][position[1] + 1]
    ):
        cost_difference = map[adjacent_node] - map[position]
        step_cost = 1 + max(0, cost_difference)
        path_cost = step_cost + cost
        tie_breaker += 1
        if heuristic == "EUCLIDIAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )

        elif heuristic == "MANHATTAN":
            heapq.heappush(
                fringe,
                (
                    path_cost + euclidian_distance(adjacent_node, end),
                    tie_breaker,
                    adjacent_node,
                ),
            )
        if (adjacent_node) not in previous_node_map or (
            adjacent_node in previous_node_map
            and previous_node_map[adjacent_node][0] > path_cost
        ):
            previous_node_map[adjacent_node] = (
                path_cost,
                position,
            )


def astar(map, size, start, end, map_original, mode, heuristic):
    goal = None
    global tie_breaker
    tie_breaker = 0
    to_visit = [(0, tie_breaker, start)]
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
        cost, _, current_node = heapq.heappop(to_visit)
        last_visit[current_node] = visit_count
        num_visits[current_node] += 1
        if visited[current_node]:
            continue
        visited[current_node] = True
        add_surrounding_nodes_to_fringe_astar(
            map,
            current_node,
            to_visit,
            size,
            visited,
            previous_node_map,
            cost,
            heuristic,
            end,
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
        cost = previous_node_map[end][0]
        x = previous_node_map[end][1][0]
        y = previous_node_map[end][1][1]
        path[x][y] = "*"
        end = previous_node_map[end][1]
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
                map_array_int[i][j] = -1
            else:
                map_array_int[i][j] = int(map_array[i][j])

    return size, start, end, map_array_int, map_array


def pathfind(mode, map_file, algorithm, heuristic=None):
    size, start, end, map, map_str = parse_map()
    if algorithm == "BFS":
        path, num_visits, visit_count, first_visit, last_visit, goal = breadth_first(
            map, size, start, end, map_str, mode
        )
        if not goal:
            print("null")
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
    elif algorithm == "UCS":
        path, num_visits, visit_count, first_visit, last_visit, goal = uniform_cost(
            map, size, start, end, map_str, mode
        )
        if not goal:
            print("null")
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
    elif algorithm == "ASTAR":
        # if heuristic != "MANHATTAN" and heuristic != "EUCLIDIAN":
        #     print(
        #         f"Invalid heuristic: {sys.argv[4]}. Valid heuristics are euclidian or manhattan (case insensitive)"
        #     )
        #     sys.exit()

        path, num_visits, visit_count, first_visit, last_visit, goal = astar(
            map, size, start, end, map_str, mode, heuristic
        )
        if not goal:
            print("null")
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
    else:
        print("Valid algorithms are BFS, UCS or A* (case insensitive)")
        sys.exit()


parse_mode(sys.argv[1].upper(), sys.argv[2], sys.argv[3].upper(), sys.argv[4].upper())
