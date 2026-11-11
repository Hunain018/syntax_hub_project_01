import heapq
maze = [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0],
    [0,1,0,1,0],
    [0,0,0,0,0]
    ]

start = (0, 0)
goal = (4, 4)

def heuristic(a, b):
    return(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(current):
    row, col = current
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]
    neighbors = []
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and maze[new_col][new_row] == 0
        ):
            neighbors.append((new_row, new_col))
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def astar(start, goal):

    open_set = []

    heapq.heappush(
        open_set,
        (heuristic(start, goal), start)
    )

    came_from = {}

    g_score = {start: 0}

    f_score = {
        start: heuristic(start, goal)
    }

    while open_set:

        current_f, current = heapq.heappop(open_set)

        # Ignore outdated entries
        if current_f != f_score[current]:
            continue

        # Goal reached
        if current == goal:

            return reconstruct_path(came_from, current)

        # Explore neighbors
        for neighbor in get_neighbors(current):

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(
                neighbor, float("inf")
            ):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score[neighbor], neighbor)
                )

    # No path available
    return None

def display_maze(maze, path, start, goal):

    for row in range(len(maze)):

        for col in range(len(maze[0])):

            position = (row, col)

            if position == start:
                print("S", end=" ")

            elif position == goal:
                print("G", end=" ")

            elif maze[row][col] == 1:
                print("#", end=" ")

            elif path and position in path:
                print("*", end=" ")

            else:
                print(".", end=" ")

        print()

print("===== A* MAZE SOLVER =====")

if (
    len(maze) == 0
    or len(maze[0]) == 0
    or any(len(row) != len(maze[0]) for row in maze)
):
    print("Invalid maze")

elif (
    not (0 <= start[0] < len(maze))
    or not (0 <= start[1] < len(maze[0]))
    or not (0 <= goal[0] < len(maze))
    or not (0 <= goal[1] < len(maze[0]))
    or maze[start[0]][start[1]] == 1
    or maze[goal[0]][goal[1]] == 1
):
    print("Invalid start or goal position")

else:

    path = astar(start, goal)

    if path is not None:

        print("\nShortest Path:")
        print(path)

        print("\nPath Length:", len(path) - 1, "moves")

        print("\nMaze Visualization:")
        display_maze(maze, path, start, goal)

    else:

        print("\nNo path found!")
        display_maze(maze, None, start, goal)
