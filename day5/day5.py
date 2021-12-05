# --- Day 5: Hydrothermal Venture ---

# You come across a field of hydrothermal vents on the ocean floor! These vents
# constantly produce large, opaque clouds, so it would be best to avoid them if
# possible.

# They tend to form in lines; the submarine helpfully produces a list of nearby
# lines of vents (your puzzle input) for you to review. For example:

# 0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2

# Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
# where x1,y1 are the coordinates of one end the line segment and x2,y2 are the
# coordinates of the other end. These line segments include the points at both
# ends. In other words:

#     An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
#     An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

# For now, only consider horizontal and vertical lines: lines where either
# x1 = x2 or y1 = y2.

# So, the horizontal and vertical lines from the above list would produce
# the following diagram:

# .......1..
# ..1....1..
# ..1....1..
# .......1..
# .112111211
# ..........
# ..........
# ..........
# ..........
# 222111....

# In this diagram, the top left corner is 0,0 and the bottom right corner is
# 9,9. Each position is shown as the number of lines which cover that point
# or . if no line covers that point. The top-left pair of 1s, for example,
# comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping
# lines 0,9 -> 5,9 and 0,9 -> 2,9.

# To avoid the most dangerous areas, you need to determine the number of
# points where at least two lines overlap. In the above example, this is
# anywhere in the diagram with a 2 or larger - a total of 5 points.

# Consider only horizontal and vertical lines. At how many points do at least
# two lines overlap?


from typing import DefaultDict


class HydroVents:
    def __init__(self) -> None:
        # use the default dict to get things initialised to 0 automatically
        self.locations = DefaultDict(lambda: 0)
        self.min_x = 0
        self.max_x = -1
        self.min_y = 0
        self.max_y = -1

    def boundary_check(self, x: int, y: int):
        if x < self.min_x:
            self.min_x = x
        if x > self.max_x:
            self.max_x = x
        if y < self.min_y:
            self.min_y = y
        if y > self.max_y:
            self.max_y = y

    def add_vent(self, x1: int, y1: int, x2: int, y2: int):
        """
        Add a vent to the map
        """
        self.boundary_check(x1, y1)
        self.boundary_check(x2, y2)

        # make sure we're running small -> big
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1

        # We will have pre-filtered here..
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.locations[(x, y)] += 1

    def new_add_vent(self, x1: int, y1: int, x2: int, y2: int):
        """
        Add a vent to the map including diagonals..
        """
        self.boundary_check(x1, y1)
        self.boundary_check(x2, y2)

        # calculate the x and y increments..
        x_inc = 0
        y_inc = 0

        if x1 < x2:
            x_inc = 1
        elif x1 > x2:
            x_inc = -1

        if y1 < y2:
            y_inc = 1
        elif y1 > y2:
            y_inc = -1

        necessary_iterations = max(abs(x2 - x1) + 1, abs(y2 - y1) + 1)
        x = x1
        y = y1

        for this_iteration in range(necessary_iterations):
            self.locations[(x, y)] += 1
            x += x_inc
            y += y_inc

    def print(self):
        """
        Output the grid
        """
        print(
            f"HydroVents Map ({self.min_x, {self.min_y}})-({self.max_x}, {self.max_y})"
        )
        for y in range(self.min_y, self.max_y + 1):
            this_row = ""
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.locations:
                    this_row += str(self.locations[(x, y)])
                else:
                    this_row += "."
            print(f"{this_row}\n")

    def count_crossovers(self):
        """
        Return the count of locations that have more than 1 vent in them..
        """
        result = 0
        for this_location in self.locations:
            if 1 < self.locations[this_location]:
                result += 1
        return result


def part1(filename: str) -> int:
    """
    Solve the part1 problem
    """
    hydro = HydroVents()
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # got a line..
                chunks = this_line.split("->")
                pt1 = chunks[0].split(",")
                pt2 = chunks[1].split(",")
                x1 = int(pt1[0])
                y1 = int(pt1[1])
                x2 = int(pt2[0])
                y2 = int(pt2[1])

                if x1 == x2 or y1 == y2:
                    # add it..
                    hydro.add_vent(x1, y1, x2, y2)

    # hydro.print()

    return hydro.count_crossovers()


def part2(filename: str) -> int:
    """
    Solve the part1 problem
    """
    hydro = HydroVents()
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # got a line..
                chunks = this_line.split("->")
                pt1 = chunks[0].split(",")
                pt2 = chunks[1].split(",")
                x1 = int(pt1[0])
                y1 = int(pt1[1])
                x2 = int(pt2[0])
                y2 = int(pt2[1])

                hydro.new_add_vent(x1, y1, x2, y2)

    return hydro.count_crossovers()


if "__main__" == __name__:
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"

    test_result = part1(test_filename)
    print(f"test_result is {test_result}")
    assert test_result == 5

    part1_result = part1(puzzle_filename)
    print(f"part1 result is {part1_result}")

    test_part2 = part2(test_filename)
    print(f"test_part2 is {test_part2}")
    assert test_part2 == 12

    part2_result = part2(puzzle_filename)
    print(f"part2 result is {part2_result}")
