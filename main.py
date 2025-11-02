import math
import random
import sys
import time
from queue import PriorityQueue


run = True
default_grid_size = (10, 10)
wall_chance = 0.05


def make_grid(size):
    x, y = size
    start = (random.randint(0, x-1), random.randint(0, y-1))
    end = (random.randint(0, x-1), random.randint(0, y-1))
    while end == start:
        end = (random.randint(0, x-1), random.randint(0, y-1))

    grid = []
    grid_pos = []
    for i in range(y):
        grid.append([])
        grid_pos.append([])
        for j in range(x):
            obj = '-'
            if random.random() < wall_chance:  # make a wall
                obj = "#"
            if (j, i) == start:
                obj = '1'
            if (j, i) == end:
                obj = '2'

            grid[i].append(obj)
            grid_pos[i].append((j, i))

    return grid, grid_pos, start, end


def print_grid(grid, Animate=False):
    for row in grid:
        for cell in row:
            print(cell, end=" ")
        print('')

    if Animate:
        # move cursor up to overwrite
        sys.stdout.write(f"\033[{len(grid) + 1}A")
        sys.stdout.flush()
        time.sleep(0.01)


def get_h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbours(pos, grid):
    positions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # up, right, left, down
    total_rows = len(grid)
    total_cols = len(grid[0])
    neighbours = []
    for x, y in positions:
        dx = x + pos[0]
        dy = y + pos[1]
        if 0 <= dx < total_cols and 0 <= dy < total_rows:
            cell = grid[dy][dx]
            if cell != "#":
                neighbours.append((dx, dy))
    return neighbours


def reconstruct_path(come_from, current):
    path = []
    while current in come_from:
        current = come_from[current]
        path.append(current)
    path.pop()
    path.reverse()
    return path


def print_reconstruct_path(path, grid):
    for x, y in path:
        grid[y][x] = '*'

    print("**Progress Complete**")
    print_grid(grid)


def algorithm(grid, grid_pos, start, end):
    open_set = PriorityQueue()
    g_scores = {pos: float('inf') for row in grid_pos for pos in row}
    g_scores[start] = 0
    f_scores = {pos: float("inf") for row in grid_pos for pos in row}
    f_scores[start] = get_h(start, end)
    come_from = {}
    count = 0
    open_set.put((0, count, start))
    open_hash = {start}
    frame_count = 0

    while not open_set.empty():
        current = open_set.get()[2]
        open_hash.remove(current)

        if current == end:
            path = reconstruct_path(come_from, current)
            print_reconstruct_path(path, grid)
            return

        # exploring begins here
        neighbours = get_neighbours(current, grid)

        for col, row in neighbours:
            temp_g_score = g_scores[current] + 1

            if temp_g_score < g_scores[(col, row)]:
                come_from[(col, row)] = current
                g_scores[(col, row)] = temp_g_score
                f_scores[(col, row)] = temp_g_score + get_h((col, row), end)
                if (col, row) not in open_hash:
                    count += 1
                    open_set.put((f_scores[(col, row)], count, (col, row)))
                    open_hash.add((col, row))

                    if (col, row) != end and (col, row) != start:  # being explored
                        grid[row][col] = "@"

        frame_count += 1
        frame_count %= 4
        # extra spaces to erase old dots
        # sys.stdout.write("\rIn Progress" + "." * frame_count + "   ")
        print('In process...')
        print_grid(grid, True)

        if current != end and current != start:  # has been explored
            grid[current[1]][current[0]] = "!"

        # print("In Progress...")
        # print_grid(grid, True)
        # print("...")

    print("!!NO PATH FOUND!!")
    print_grid(grid)


while run:
    print("---")
    grid = None
    start = None
    end = None

    grid_size = input(
        "Enter the coustom grid size (x,y) / Press Enter for Default(10, 10): ")

    if grid_size:
        try:
            x, y = grid_size.split(",")
            grid_size = (int(x), int(y))
            wall_chance += (int(x) + int(y)) / 1000
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a comma.")
            continue
    else:
        grid_size = default_grid_size

    while True:
        grid, grid_pos, start, end = make_grid(grid_size)
        print("Selecting...")
        print_grid(grid)
        select_grid = input("Continue with current grid(y/n): ")
        if select_grid.lower() == "y":
            break

    algorithm(grid, grid_pos, start, end)

    restart = input("Run an another stimulation(y/n): ")
    if restart.lower() == "y":
        continue
    run = False
