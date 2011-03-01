import random

class LifeManager(object):

    def __init__(self, width = 100, height = 100, born_if = (3,), alive_if = (2, 3)):

        self._width = width
        self._height = height
        self._born_if = born_if
        self._alive_if = alive_if
        self._cells = []

        self._cells = self.getEmptyLife()
        self.randomSeed()

    def createCell(self):
        return 1

    def getEmptyLife(self):
        cells = [None] * self._width
        for x in xrange(self._width):
            cells[x] = [None] * self._height
        return cells

    def randomSeed(self):
        amount = 300
        square = 20
        if square is None:
            width = self._width
            height = self._height
        else:
            width = square
            height = square
        x0 = random.randint(0, self._width - width)
        y0 = random.randint(0, self._height - height)
        for _ in xrange(amount):
            x = x0 + random.randint(0, width - 1)
            y = y0 + random.randint(0, height - 1)
            self._cells[x][y] = self.createCell()

    def width(self):
        return self._width

    def height(self):
        return self._height

    def cell(self, x, y):
        return self._cells[x][y]

    def isAlive(self, x, y):
        """Returns True if cell is alive"""
        if self._cells[x][y]:
            return True
        else:
            return False

    def color(self, x, y):
        """Returns color of the cell as a tuple (red, green, blue)"""
        if not self.isAlive(x, y):
            return (0, 0, 0)
        else:
            return (255, 255, 255)

    def next(self):
        """Calculates the next stage of the life"""

        # New life
        new_cells = self.getEmptyLife()

        # Calculate state of all cells in the new life
        for x in xrange(self._width):
            for y in xrange(self._height):

                # Calculate number of neighbors

                neighbors = 0

                dx_set = [0]
                if x > 0: dx_set.append(-1)
                if x < self._width - 1: dx_set.append(1)

                dy_set = [0]
                if y > 0: dy_set.append(-1)
                if y < self._height - 1: dy_set.append(1)

                for dx in dx_set:
                    for dy in dy_set:
                        if (dx or dy) and self._cells[x + dx][y + dy]:
                            neighbors += 1

                # Cell is alive, should it die?
                if self._cells[x][y]:
                    if neighbors in self._alive_if:
                        new_cells[x][y] = 1
                    else:
                        new_cells[x][y] = None

                # Cell is dead, should it born?
                else:
                    if neighbors in self._born_if:
                        new_cells[x][y] = 1
                    else:
                        new_cells[x][y] = None

        # Replace old life with the new one
        self._cells = new_cells
