from p5 import *
from random import choice

HEIGHT = 800
WIDTH = 1600
ROWS = 20
COLUMNS = 40
CELL_SIZE = HEIGHT / ROWS


class Cell:
    OPPOSITE = {'left': 'right', 'right': 'left', 'top': 'bottom', 'bottom': 'top'}

    def __init__(self, x, y):
        self.neighbours = {'closed': [], 'open': [], 'visited': set()}
        self.x = x
        self.y = y
        self.walls = {'left': True, 'right': True, 'top': True, 'bottom': True}  # top, right, bottom, left - clockwise
        self.tr_corner = (self.x * CELL_SIZE + CELL_SIZE, self.y * CELL_SIZE)
        self.tl_corner = (self.x * CELL_SIZE, self.y * CELL_SIZE)
        self.br_corner = (self.x * CELL_SIZE + CELL_SIZE, self.y * CELL_SIZE + CELL_SIZE)
        self.bl_corner = (self.x * CELL_SIZE, self.y * CELL_SIZE + CELL_SIZE)
        self.visited = 0
        self.previous = self
        self.is_drawn = 0

    def __str__(self):
        return f'x:{self.x} y:{self.y} index: {self.index}\n'

    def __repr__(self):
        return self.__str__()

    def draw(self):
        if self.is_drawn < 2:
            if self.visited and self.is_drawn == 0:
                color_mode('HSB')
                fill(200, 100, 200)

                rect(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE, CELL_SIZE,
                     mode=CENTER)
                no_stroke()
                rect(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2, CELL_SIZE + 1,
                     CELL_SIZE + 1, mode=CENTER)

                stroke(1)
                stroke_weight(1)

            if self.walls['left']:
                line(self.tl_corner, self.bl_corner)
            if self.walls['right']:
                line(self.tr_corner, self.br_corner)
            if self.walls['top']:
                line(self.tl_corner, self.tr_corner)
            if self.walls['bottom']:
                line(self.bl_corner, self.br_corner)

            self.is_drawn += 1

    def generate_neighbours(self, size_x, size_y):
        if self.x != 0:
            self.neighbours['closed'].append('left')
        if self.y != 0:
            self.neighbours['closed'].append('top')
        if self.x < size_x - 1:
            self.neighbours['closed'].append('right')
        if self.y < size_y - 1:
            self.neighbours['closed'].append('bottom')

    def open_neighbour(self, neighbour, side):
        self.neighbours['closed'].remove(side)
        self.neighbours['open'].append(side)
        self.walls[side] = False
        neighbour.neighbours['closed'].remove(Cell.OPPOSITE[side])
        neighbour.neighbours['open'].append(Cell.OPPOSITE[side])
        neighbour.walls[Cell.OPPOSITE[side]] = False


class Maze:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.cells = []
        for y in range(self.size_y):
            for x in range(self.size_x):
                self.cells.append(Cell(x, y))
        self.visited = []
        self.stack = []
        self.current = choice(self.cells)

    def walk(self):
        if self.current is None:
            return
        self.current.visited = True

        while True:
            if self.current.neighbours['visited'] != set(self.current.neighbours['closed']):
                side = choice(self.current.neighbours['closed'])
                if side == 'top':
                    next_cell = m.cells[m.find_index(self.current.x, self.current.y - 1)]
                elif side == 'bottom':
                    next_cell = m.cells[m.find_index(self.current.x, self.current.y + 1)]
                elif side == 'right':
                    next_cell = m.cells[m.find_index(self.current.x + 1, self.current.y)]
                elif side == 'left':
                    next_cell = m.cells[m.find_index(self.current.x - 1, self.current.y)]
                if next_cell.visited:
                    self.current.neighbours['visited'].add(side)
                else:
                    break
            else:
                self.current = self.current.previous

        self.current.open_neighbour(next_cell, side)
        next_cell.previous = self.current
        self.current = next_cell
        self.current.visited = True

    def find_index(self, x, y):
        index = 0
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return index
            index += 1

    def find_neighbours(self):
        for cell in self.cells:
            cell.generate_neighbours(self.size_x, self.size_y)
            print(cell.neighbours)

    @staticmethod
    def open_neighbours(cell1, cell2):
        cell1.open_neighbours.add(cell2.index)
        cell1.closed_neighbours.remove(cell2.index)
        cell2.open_neighbours.add(cell1.index)
        cell2.closed_neighbours.remove(cell1.index)

    def draw_cells(self):
        for cell in self.cells:
            if cell.is_drawn < 2 and cell.visited is True:
                cell.draw()


m = Maze(COLUMNS, ROWS)
m.find_neighbours()


def setup():
    size(WIDTH, HEIGHT)
    stroke(1)
    background(204, )


def draw():
    for cell in m.cells:
        if not cell.visited:
            m.walk()
            break

    m.draw_cells()


run()
