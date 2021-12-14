# --- Day 13: Transparent Origami ---

# You reach another volcanically active part of the cave. It would be nice if
# you could do some kind of thermal imaging so you could tell ahead of time
# which caves are too hot to safely enter.

# Fortunately, the submarine seems to be equipped with a thermal camera! When
# you activate it, you are greeted with:

# Congratulations on your purchase! To activate this infrared thermal imaging
# camera system, please enter the code found on page 1 of the manual.

# Apparently, the Elves have never used this feature. To your surprise, you
# manage to find the manual; as you go to open it, page 1 falls out. It's a
# large sheet of transparent paper! The transparent paper is marked with random
# dots and includes instructions on how to fold it up (your puzzle input).
# For example:

# 6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0

# fold along y=7
# fold along x=5

# The first section is a list of dots on the transparent paper. 0,0 represents
# the top-left coordinate. The first value, x, increases to the right. The
# second value, y, increases downward. So, the coordinate 3,0 is to the right
# of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example
# form the following pattern, where # is a dot on the paper and . is an empty,
# unmarked position:

# ...#..#..#.
# ....#......
# ...........
# #..........
# ...#....#.#
# ...........
# ...........
# ...........
# ...........
# ...........
# .#....#.##.
# ....#......
# ......#...#
# #..........
# #.#........

# Then, there is a list of fold instructions. Each instruction indicates a line
# on the transparent paper and wants you to fold the paper up (for horizontal
# y=... lines)
# or left (for vertical x=... lines).
# In this example, the first fold instruction is fold along y=7, which
# designates the line formed by all of the positions where y is 7
# (marked here with -):

# ...#..#..#.
# ....#......
# ...........
# #..........
# ...#....#.#
# ...........
# ...........
# -----------
# ...........
# ...........
# .#....#.##.
# ....#......
# ......#...#
# #..........
# #.#........

# Because this is a horizontal line, fold the bottom half up. Some of the dots
# might end up overlapping after the fold is complete, but dots will never
# appear exactly on a fold line. The result of doing this fold looks like this:

# #.##..#..#.
# #...#......
# ......#...#
# #...#......
# .#.#..#.###
# ...........
# ...........

# Now, only 17 dots are visible.

# Notice, for example, the two dots in the bottom left corner before the
# transparent paper is folded; after the fold is complete, those dots appear in
# the top left corner (at 0,0 and 0,1). Because the paper is transparent, the
# dot just below them in the result (at 0,3) remains visible, as it can be seen
# through the transparent paper.

# Also notice that some dots can end up overlapping; in this case, the dots
# merge together and become a single dot.

# The second fold instruction is fold along x=5, which indicates this line:

# #.##.|#..#.
# #...#|.....
# .....|#...#
# #...#|.....
# .#.#.|#.###
# .....|.....
# .....|.....

# Because this is a vertical line, fold left:

# #####
# #...#
# #...#
# #...#
# #####
# .....
# .....

# The instructions made a square!

# The transparent paper is pretty big, so for now, focus on just completing the
# first fold. After the first fold in the example above, 17 dots are visible -
# dots that end up overlapping after the fold is completed count as a single
# dot.

# How many dots are visible after completing just the first fold instruction on
# your transparent paper?


class TransparentPaper:
    def __init__(self) -> None:
        self.dots = dict()
        self.min_x = 0
        self.max_x = -1
        self.min_y = 0
        self.max_y = -1
        self.instructions = []

    def __repr__(self) -> str:
        result = f"TransparentPaper<{self.max_x-self.min_x}x{self.max_y-self.min_y}, {self.count_dots()} dots>\n"
        for y in range(self.min_y, self.max_y + 1):
            s = ""
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.dots:
                    s += "#"
                else:
                    s += "."
            result += f"{s}\n"
        return result

    def set_dot(self, x: int, y: int):
        """
        Shade in a dot
        """
        key = (x, y)
        if key not in self.dots:
            self.dots[key] = 1
        else:
            self.dots[key] += 1
        # and sort the bounds..
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def remove_dot(self, x: int, y: int):
        """
        completely remove a dot
        """
        key = (x, y)
        if key in self.dots:
            del self.dots[key]

    def fold(self, fold_x=None, fold_y=None):
        """
        Fold either vertically or horizontally
        """
        for x, y in list(self.dots):
            new_x = None
            new_y = None
            if fold_x is not None and x > fold_x:
                new_x = fold_x - (x - fold_x)
                new_y = y
            elif fold_y is not None and y > fold_y:
                new_x = x
                new_y = fold_y - (y - fold_y)
            # do we have a new target ?
            if new_x is not None:
                self.set_dot(new_x, new_y)
                self.remove_dot(x, y)

        # and fix the display
        if fold_x is not None:
            self.max_x = fold_x
        if fold_y is not None:
            self.max_y = fold_y

    def count_dots(self):
        return len(self.dots)

    def load_file(self, filename: str):
        """
        Read all the dots and put them on the paper
        additionally populate the instructions list with the folds
        """
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # What sort of line is it ?
                    if this_line.startswith("fold along"):
                        self.instructions.append(this_line)
                    else:
                        vals = this_line.split(",")
                        x = int(vals[0])
                        y = int(vals[1])
                        self.set_dot(x, y)

    def run_instructions(self, number_to_run=None):
        """
        Run a number of instructions (or all if not specified)
        """
        while (number_to_run is None or number_to_run > 0) and 0 < len(
            self.instructions
        ):
            # get one instruction..
            this_instruction = self.instructions[0]
            self.instructions = self.instructions[1:]

            # run one instruction..
            print(f"Running: {this_instruction}")
            # fold along x=1
            parts = this_instruction.split("=")
            axis = parts[0][-1]
            index = int(parts[1])
            print(f"Gonna be flexing along the {axis} axis at index {index}")
            if "x" == axis:
                self.fold(fold_x=index)
            elif "y" == axis:
                self.fold(fold_y=index)
            else:
                raise ValueError(f"What the actual hell is a fold of {axis}")

            # decrement accordingly
            if number_to_run is not None:
                number_to_run -= 1


def part1(filename: str):
    """
    Solve part1
    """
    paper = TransparentPaper()
    paper.load_file(filename)
    print(paper)
    paper.run_instructions(1)
    print(paper)

    return paper.count_dots()


def part2(filename: str):
    """
    Solve part1
    """
    paper = TransparentPaper()
    paper.load_file(filename)
    print(paper)
    paper.run_instructions()
    print(paper)

    return paper.count_dots()


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test1_expected = 17

    test1 = part1(test_filename)
    print(f"test1 got {test1}, expected {test1_expected}")
    assert test1 == test1_expected

    puzz1 = part1(puzzle_filename)
    print(f"Part1 is {puzz1}")

    puzz2 = part2(puzzle_filename)
