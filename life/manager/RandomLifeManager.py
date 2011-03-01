import random
import math
from LifeManager import LifeManager

class RandomLifeManager(LifeManager):

    def randomSeed(self):
        for color in (0.0, 0.33, 0.67):
            amount = 100
            square = 15
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
                self._cells[x][y] = self.createCell(0.5, color)

    def __init__(self, *args, **kwargs):
        super(RandomLifeManager, self).__init__(*args, **kwargs)
        self._cells_count = 0

    def createCell(self, energy = 0.5, color = 0.3):
        """Creates a new cell (green cell with average energy by default"""
        if energy <= 0:
            return None
        if energy > 1:
            energy = 1
        while color < 0:
            color += 1
        while color > 1:
            color -= 1
        return (energy, color)

    def cellEnergy(self, x, y):
        """Returns cell's energy"""
        cell = self.cell(x, y)
        if cell:
            return cell[0]
        else:
            return 0.0

    def cellColor(self, x, y):
        """Returns cell's color"""
        cell = self.cell(x, y)
        if cell:
            return cell[1]
        else:
            return 0.0

    def color(self, x, y):
        """Returns color of the cell as a tuple (red, green, blue)"""

        # Dead cell?
        if not self._cells[x][y]:
            return (0, 0, 0)

        # Cell brightness
        #minBrightness = 32
        #maxBrightness = 255
        #brightness = int(minBrightness + self.cellEnergy(x, y) * (maxBrightness - minBrightness))
        brightness = self.cellEnergy(x, y)
        # Normalize brightness
        brightness = 0.2 + 0.7 * brightness

        # Cell hue
        hue = self.cellColor(x, y)

        # We assume saturation is always at maximum
        saturation = 1.0

        # Convert HSB -> RGB
        if brightness < 0.5:
            temp2 = brightness * (1.0 + saturation)
        else:
            temp2 = brightness + saturation - brightness * saturation
        temp1 = 2.0 * brightness - temp2
        color = [hue + 1.0 / 3.0, hue, hue - 1.0 / 3.0]
        for x in (0, 1, 2):
            c = color[x]
            if c < 0:
                c += 1.0
            elif c > 1:
                c -= 1.0
            if 6.0 * c < 1:
                c = temp1 + (temp2 - temp1) * 6.0 * c
            elif 2.0 * c < 1:
                c = temp2
            elif 3.0 * c < 2:
                c = temp1 + (temp2 - temp1) * ((2.0/3.0) - c) * 6.0
            else:
                c = temp1
            c = int(255 * c)
            color[x] = c

        return color

    def next(self):
        """Calculates the next stage of the life"""

        # Life settings
        optimal_alive_cells_ratio = 0.1
        max_color_mutation = 0.01
        energy_hit_on_death = 0.75
        newborn_energy = 0.5
        max_energy_hit_for_parents_color_diff = 10.0
        max_energy_hit_for_overcrowding = 0.25

        # New life
        cells = self._cells
        new_cells = self.getEmptyLife()
        cells_count = 0

        # Data for energy compensation based on total number of cells
        alive_cells_ratio = float(self._cells_count) / (self.width() * self.height())
        # 1.0 for empty field; 0.0 for optimal ratio, <0.0 for too crowded field
        alive_cells_max_energy_shift = 1.0 - alive_cells_ratio / optimal_alive_cells_ratio

        # Calculate state of all cells in the new life
        for x in xrange(self._width):
            for y in xrange(self._height):

                # Calculate amount and other statistics of neighbors

                neighbors_count = 0
                neighbors_energy = 0.0
                neighbors_color = (0.0, 0.0)

                dx_set = [0]
                if x > 0: dx_set.append(-1)
                if x < self._width - 1: dx_set.append(1)

                dy_set = [0]
                if y > 0: dy_set.append(-1)
                if y < self._height - 1: dy_set.append(1)

                for dx in dx_set:
                    for dy in dy_set:
                        if (dx or dy) and cells[x + dx][y + dy]:
                            neighbors_count += 1
                            neighbors_energy += self.cellEnergy(x + dx, y + dy)
                            neighbors_color = self.getColorVector(neighbors_color, cells[x + dx][y + dy])

                neighbors_color_power, neighbors_color_hue = neighbors_color

                if neighbors_count == 0:
                    neighbors_average_energy = 0
                else:
                    neighbors_average_energy = neighbors_energy / neighbors_count

                # Cell was alive
                if cells[x][y]:

                    # Current energy
                    energy = self.cellEnergy(x, y)

                    # Random energy change based on the number of neighbors
                    # Energy increases in empty environments and decreases in crowded
                    neighbors_energy_shift = (5 - neighbors_count) / 100.0 # -0.03..0.05
                    energy += random.uniform(neighbors_energy_shift - 0.02, neighbors_energy_shift + 0.02)

                    # Random energy change based on the total number of alive cells
                    if alive_cells_max_energy_shift < 0:
                        energy += random.uniform(max_energy_hit_for_overcrowding * alive_cells_max_energy_shift, 0)

                    #total_energy_shift =

                    # Kill cell by decreasing its energy
                    if neighbors_count not in self._alive_if:
                        energy -= energy_hit_on_death

                    # Color mutation
                    color = self.cellColor(x, y)
                    color += random.uniform(-max_color_mutation, max_color_mutation)

                    # New cell (dead or alive)
                    new_cells[x][y] = self.createCell(energy, color)


                # Cell was dead
                else:

                    # Color of the new cell
                    color = neighbors_color_hue

                    if neighbors_count in self._born_if:

                        # Born new cell
                        energy = newborn_energy

                        # Add up to 0.1 energy if parents are energetic
                        energy += neighbors_average_energy / 10

                        # Subtract energy if parents are of too different colors
                        # Newborn children might be even dead
                        # 0.0 - same colors, 1.0 - opposite colors
                        color_diff = 1 - neighbors_color_power / neighbors_energy
                        energy -= max_energy_hit_for_parents_color_diff * color_diff

                    elif (neighbors_average_energy > 0.9) and (random.random() > neighbors_count / 10):

                        # Sometimes weak cell may be born even when it shouldn't
                        # It is much more likely in crowded environments
                        energy = neighbors_average_energy / 10

                    else:

                        # Keep cell dead
                        energy = 0

                    # Store new cell
                    new_cells[x][y] = self.createCell(energy, color)

                # Count alive cells
                if new_cells[x][y]:
                    cells_count += 1

        # Replace old life with the new one
        self._cells = new_cells

        # Add random cells if there is no life
        if cells_count == 0 and random.random() < 0.02:
            self.randomSeed()

        self._cells_count = cells_count

    def getColorVector(self, vector, cell):
        """Get new color vector"""

        r1 = vector[0]
        a1 = vector[1] * 2.0 * math.pi

        r2 = cell[0]
        a2 = cell[1] * 2.0 * math.pi

        x = r1 * math.cos(a1) + r2 * math.cos(a2)
        y = r1 * math.sin(a1) + r2 * math.sin(a2)

        r = math.sqrt(x * x + y * y)
        if x != 0.0:
            a = math.atan(y / x)
            # atan disambiguation
            if x < 0 and y > 0 and a < 0:
                a += math.pi
            elif x < 0 and y < 0 and a > 0:
                a += math.pi
        elif y > 0:
            a = math.pi / 2.0
        else:
            a = -math.pi / 2.0

        return (r, a / 2.0 / math.pi)

