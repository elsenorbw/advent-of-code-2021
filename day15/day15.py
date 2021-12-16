# --- Day 15: Chiton ---

# You've almost reached the exit of the cave, but the walls are getting closer
# together. Your submarine can barely still fit, though; the main problem is
# that the walls of the cave are covered in chitons, and it would be best not
# to bump any of them.

# The cavern is large, but has a very low ceiling, restricting your motion to
# two dimensions. The shape of the cavern resembles a square; a quick scan of
# chiton density produces a map of risk level throughout the cave (your puzzle
# input). For example:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581

# You start in the top left position, your destination is the bottom right
# position, and you cannot move diagonally. The number at each position is its
# risk level; to determine the total risk of an entire path, add up the risk
# levels of each position you enter (that is, don't count the risk level of
# your starting position unless you enter it; leaving it adds no risk to your
# total).

# Your goal is to find a path with the lowest total risk. In this example, a
# path with the lowest total risk is highlighted here:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581

# The total risk of this path is 40 (the starting position is never entered,
# so its risk is not counted).

# What is the lowest total risk of any path from the top left to the bottom
# right?


from typing import Dict, List


class MapThing:
    def __init__(self) -> None:
        self.grid = dict()
        self.min_x = 0
        self.max_x = -1
        self.min_y = 0
        self.max_y = -1

    def print(self):
        """
        Just simple output..
        """
        print(f"MapThing {self.max_x-self.min_x + 1}x{self.max_y - self.min_y + 1}")
        for y in range(self.min_y, self.max_y + 1):
            s = ""
            for x in range(self.min_x, self.max_x + 1):
                s += str(self.grid[(x, y)])
            print(s)

    def store_danger(self, x: int, y: int, danger_level: int):
        """
        Add this to the map
        """
        self.grid[(x, y)] = danger_level
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def load_file(self, filename: str):
        """
        Load the map from the file
        """
        with open(filename, "r") as f:
            y = 0
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    for x, the_val in enumerate(this_line):
                        self.store_danger(x, y, int(the_val))
                    y += 1

    def find_safest(
        self,
        x: int,
        y: int,
        steps_so_far: List,
        danger_so_far: int,
        best_path_record: Dict,
    ):
        """
        The recursive wandering chunk..
        """
        key = (x, y)

        # 0) Are we off the grid ?
        if key not in self.grid:
            return

        this_danger = danger_so_far + self.grid[key]

        # and are we just wating our time ?
        if this_danger >= self.best_danger:
            return

        # 1) Check whether we've been here before or better
        if key in best_path_record:
            if best_path_record[key] < this_danger:
                # we have already been here more efficiently, we're done..
                return

        # 2) Check we haven't been here before..
        # Actually, this is probably impossible..
        # going to assert that's the case and figure it out later if not..
        # assert key not in steps_so_far

        # 3) ok, we should do work from here..
        best_path_record[key] = this_danger
        steps_so_far.append(key)

        # 4) Was this the final step ?
        if self.max_x == x and self.max_y == y:
            print(f"Storing a final path with danger {this_danger} : {steps_so_far}")
            self.best_danger = this_danger
        else:
            # We can now move out and try all the different directions..
            self.find_safest(x + 1, y, steps_so_far, this_danger, best_path_record)
            self.find_safest(x, y + 1, steps_so_far, this_danger, best_path_record)
            self.find_safest(x - 1, y, steps_so_far, this_danger, best_path_record)
            self.find_safest(x, y - 1, steps_so_far, this_danger, best_path_record)

        # 5) and allow recursion to be cool..
        steps_so_far.pop()
        return

    def calculate_safest_route(self):
        """
        Calculate the safest route to the bottom right of the map
        start at the top-left
        """
        # basic plan, go right, go down, go left, go up
        # if we have been to a location more efficiently then we can stop
        # if we have reached the end more safely than our current move then
        # also time to stop.
        # shortest route should end quite quickly (maybe)
        self.best_danger = 9999999999
        current_x = self.min_x
        current_y = self.min_y

        steps_so_far = [(current_x, current_y)]
        danger_so_far = 0  # no danger for the first step..
        best_path_record = dict()  # no idea what the best path to anywhere is so far..

        # first try going right..
        self.find_safest(
            current_x + 1, current_y, steps_so_far, danger_so_far, best_path_record
        )

        # and now try starting down..
        self.find_safest(
            current_x, current_y + 1, steps_so_far, danger_so_far, best_path_record
        )

        # and we're done.. what's the most efficient to the bottom right ?

        return self.best_danger


def part1(filename: str) -> int:
    """
    Run the part1 solution
    """
    cavern = MapThing()
    cavern.load_file(filename)
    cavern.print()
    cavern.calculate_safest_route()

    return cavern.best_danger


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test1_expected = 40

    test1 = part1(test_filename)
    print(f"Test part1 returned {test1}, should have been {test1_expected}")
    assert test1 == test1_expected

    puzz1 = part1(puzzle_filename)
    print(f"Part1 actual result : {puzz1}")
