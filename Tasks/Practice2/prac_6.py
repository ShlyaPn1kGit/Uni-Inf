import pygame
import random
import math
from queue import PriorityQueue
from collections import deque

pygame.init()

WIDTH = 600
GRID_SIZE = 15
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A*")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
VISITED = 5
OPEN = 6

# Параметры

class Cell: # Хранит данные о клетке 
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.color = WHITE
        self.state = EMPTY

    def get_pos(self):
        return self.row, self.col

    def is_empty(self):
        return self.state == EMPTY

    def is_barrier(self):
        return self.state == OBSTACLE

    def is_start(self):
        return self.state == START

    def is_end(self):
        return self.state == END

    def is_path(self):
        return self.state == PATH

    def is_visited(self):
        return self.state == VISITED

    def is_open(self):
        return self.state == OPEN

    def reset(self):
        self.color = WHITE
        self.state = EMPTY

    def make_start(self):
        self.color = ORANGE
        self.state = START

    def make_end(self):
        self.color = TURQUOISE
        self.state = END

    def make_barrier(self):
        self.color = BLACK
        self.state = OBSTACLE

    def make_path(self):
        self.color = PURPLE
        self.state = PATH

    def make_visited(self):
        self.color = GREEN
        self.state = VISITED

    def make_open(self):
        self.color = YELLOW
        self.state = OPEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))


def make_grid(): # функция генерации массива для задания
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid


def draw_grid(win, grid): # Отрисовка карты
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)

    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()


def generate_random_grid(grid): # наполнение карты случайными препятсвиями
    for row in grid:
        for cell in row:
            cell.reset()

    start_row, start_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_start()
    end.make_end()

    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.2)
    for _ in range(obstacle_count):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        cell = grid[row][col]
        if not cell.is_start() and not cell.is_end():
            cell.make_barrier()

    return start, end


def compute_distance_map(grid, end_cell):
    dist = [[math.inf] * GRID_SIZE for _ in range(GRID_SIZE)]
    ex, ey = end_cell.get_pos()
    dist[ex][ey] = 0
    q = deque([(ex, ey)])

    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny].is_barrier():
                    continue
                if dist[nx][ny] > dist[x][y] + 1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
    return dist


def h(cell1, dist_map):
    x, y = cell1.get_pos()
    return dist_map[x][y]


def get_neighbors(grid, cell):
    x, y = cell.get_pos()
    neighbors = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbor = grid[nx][ny]
            if not neighbor.is_barrier():
                neighbors.append(neighbor)
    return neighbors


def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        current = came_from[current]
        if current.is_start():
            break
        current.make_path()
        path.append(current)
        draw()
    return path


def a_star(draw, grid, start, end, dist_map):
    count = 0
    # Открытый список: (f_score, count, cell), приоритет по f_score
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    # came_from[cell] — для восстановления пути
    came_from = {}
    # g_score — стоимость пути от старта (у старта 0, у остальных бесконечность)
    g_score = {cell: math.inf for row in grid for cell in row}
    g_score[start] = 0

    # f_score = g + h — оценка полной стоимости пути через ячейку
    f_score = {cell: math.inf for row in grid for cell in row}
    f_score[start] = h(start, dist_map)

    # ячейки, лежащие в open_set
    open_set_hash = {start}

    while not open_set.empty():
        # на случай закрытия окна во время работы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        # берём ячейку с наименьшим f_score
        current = open_set.get()[2]
        open_set_hash.discard(current)

        # после нахождения пути визуализируем его
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return g_score[end]

        # перебор соседей
        for neighbor in get_neighbors(grid, current):
            temp_g = g_score[current] + 1

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor, dist_map)

                # Если соседа ещё нет в открытом списке — добавляем
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()  # жёлтый — в открытом списке
        draw()
        if current != start:
            current.make_visited()  # зелёный — обработана

    # на случай если пути нет.
    return None


def main():
    grid = make_grid()
    start, end = generate_random_grid(grid)
    dist_map = compute_distance_map(grid, end)

    draw = lambda: draw_grid(WIN, grid)

    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start, end = generate_random_grid(grid)
                    dist_map = compute_distance_map(grid, end)
                if event.key == pygame.K_SPACE:
                    result = a_star(draw, grid, start, end, dist_map)
                    if result is not None:
                        print(f"Расстояние: {int(result)}")
                    else:
                        print("Путь не найден.")

    pygame.quit()


if __name__ == "__main__":
    main()
