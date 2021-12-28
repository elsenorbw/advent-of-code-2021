# --- Day 20: Trench Map ---

# With the scanners fully deployed, you turn their attention to mapping the floor of the ocean trench.

# When you get back the image from the scanners, it seems to just be random noise. Perhaps you can combine an image enhancement algorithm and the input image (your puzzle input) to clean it up a little.

# For example:

# ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
# #..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
# .######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
# .#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
# .#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
# ...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
# ..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

# #..#.
# #....
# ##..#
# ..#..
# ..###

# The first section is the image enhancement algorithm. It is normally given on a single line, but it has been wrapped to multiple lines in this example for legibility. The second section is the input image, a two-dimensional grid of light pixels (#) and dark pixels (.).

# The image enhancement algorithm describes how to enhance an image by simultaneously converting all pixels in the input image into an output image. Each pixel of the output image is determined by looking at a 3x3 square of pixels centered on the corresponding input image pixel. So, to determine the value of the pixel at (5,10) in the output image, nine pixels from the input image need to be considered: (4,9), (4,10), (4,11), (5,9), (5,10), (5,11), (6,9), (6,10), and (6,11). These nine input pixels are combined into a single binary number that is used as an index in the image enhancement algorithm string.

# For example, to determine the output pixel that corresponds to the very middle pixel of the input image, the nine pixels marked by [...] would need to be considered:

# # . . # .
# #[. . .].
# #[# . .]#
# .[. # .].
# . . # # #

# Starting from the top-left and reading across each row, these pixels are ..., then #.., then .#.; combining these forms ...#...#.. By turning dark pixels (.) into 0 and light pixels (#) into 1, the binary number 000100010 can be formed, which is 34 in decimal.

# The image enhancement algorithm string is exactly 512 characters long, enough to match every possible 9-bit binary number. The first few characters of the string (numbered starting from zero) are as follows:

# 0         10        20        30  34    40        50        60        70
# |         |         |         |   |     |         |         |         |
# ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##

# In the middle of this first group of characters, the character at index 34 can be found: #. So, the output pixel in the center of the output image should be #, a light pixel.

# This process can then be repeated to calculate every pixel of the output image.

# Through advances in imaging technology, the images being operated on here are infinite in size. Every pixel of the infinite output image needs to be calculated exactly based on the relevant pixels of the input image. The small input image you have is only a small region of the actual infinite input image; the rest of the input image consists of dark pixels (.). For the purposes of the example, to save on space, only a portion of the infinite-sized input and output images will be shown.

# The starting input image, therefore, looks something like this, with more dark pixels (.) extending forever in every direction not shown here:

# ...............
# ...............
# ...............
# ...............
# ...............
# .....#..#......
# .....#.........
# .....##..#.....
# .......#.......
# .......###.....
# ...............
# ...............
# ...............
# ...............
# ...............

# By applying the image enhancement algorithm to every pixel simultaneously, the following output image can be obtained:

# ...............
# ...............
# ...............
# ...............
# .....##.##.....
# ....#..#.#.....
# ....##.#..#....
# ....####..#....
# .....#..##.....
# ......##..#....
# .......#.#.....
# ...............
# ...............
# ...............
# ...............

# Through further advances in imaging technology, the above output image can also be used as an input image! This allows it to be enhanced a second time:

# ...............
# ...............
# ...............
# ..........#....
# ....#..#.#.....
# ...#.#...###...
# ...#...##.#....
# ...#.....#.#...
# ....#.#####....
# .....#.#####...
# ......##.##....
# .......###.....
# ...............
# ...............
# ...............

# Truly incredible - now the small details are really starting to come through. After enhancing the original input image twice, 35 pixels are lit.

# Start with the original input image and apply the image enhancement algorithm twice, being careful to account for the infinite size of the images. How many pixels are lit in the resulting image?


class Enhancer:
    def __init__(self, enhancer: str) -> None:
        assert len(enhancer) == 512
        self.yields_lit = set()
        for idx, val in enumerate(enhancer):
            if val == "#":
                self.yields_lit.add(idx)

    def pixel_for(self, index):
        """
        Returns True if the pixel should be lit
        """
        return index in self.yields_lit


class Image:
    def __init__(self) -> None:
        self.pixels = set()
        self.min_x = 0
        self.max_x = -1
        self.min_y = 0
        self.max_y = -1
        # sometimes the infinity pixels are non-empty
        self.out_of_bounds_default = False

    def is_lit(self, x, y):
        if x < self.min_x or x > self.max_x or y < self.min_y or y > self.max_y:
            result = self.out_of_bounds_default
        else:
            result = (x, y) in self.pixels
        return result

    def print(self):
        print(f"Image ({self.min_x}, {self.min_y})-({self.max_x}, {self.max_y})")
        for y in range(self.min_y, self.max_y + 1):
            s = ""
            for x in range(self.min_x, self.max_x + 1):
                if self.is_lit(x, y):
                    s += "#"
                else:
                    s += "."
            print(s)

    def count_lit_pixels(self):
        """
        How many are lit ?
        """
        return len(self.pixels)

    def set_pixel(self, x, y):
        """
        Set a pixel into the lit state
        """
        self.pixels.add((x, y))
        if x < self.min_x:
            self.min_x = x
        if x > self.max_x:
            self.max_x = x
        if y < self.min_y:
            self.min_y = y
        if y > self.max_y:
            self.max_y = y

    def get_enhancer_value(self, x, y):
        """
        Get the values based on the surrounding pixels..
        """
        locations = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
        result = 0
        for this_x, this_y in locations:
            result *= 2
            if self.is_lit(this_x, this_y):
                result += 1
        return result

    def enhance(self, enhancer):
        """
        Use the enhancer to create a new, enhanced image
        """
        result = Image()
        # and set the default pixel values.. these should toggle on and off in certain situations..
        if enhancer.pixel_for(0):
            # ok, so blank pixels should turn into lit pixels..
            assert not enhancer.pixel_for(511)
            # and toggle the current setting:
            result.out_of_bounds_default = not self.out_of_bounds_default

        for x in range(self.min_x - 1, self.max_x + 2):
            for y in range(self.min_y - 1, self.max_y + 2):
                # get the enhancer value for this location
                enhancer_value = self.get_enhancer_value(x, y)
                # is the new pixel lit ?
                if enhancer.pixel_for(enhancer_value):
                    result.set_pixel(x, y)

        return result


def partx(filename: str, enhancement_count: int):
    # Load the input and get an enhancer and initial image
    enhancer = None
    image = Image()

    # wander through the file
    y = 0
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # ok, do we need an enhancer ?
                if enhancer is None:
                    enhancer = Enhancer(this_line)
                else:
                    # ok, we're on the way through the picture grid..
                    for x, val in enumerate(this_line):
                        if val == "#":
                            image.set_pixel(x, y)
                    y += 1
    image.print()

    # enhance it twice..
    for i in range(enhancement_count):
        image = image.enhance(enhancer)

    # and count the lit pixels
    result = image.count_lit_pixels()
    return result


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test1_expected = 35
    puzz1_expected = 5563
    test2_expected = 3351

    test1 = partx(test_filename, 2)
    print(f"Test1 got {test1}, expected {test1_expected}")
    assert test1 == test1_expected

    puzz1 = partx(puzzle_filename, 2)
    print(f"Puzzle1 is {puzz1}")
    assert puzz1 == puzz1_expected

    test2 = partx(test_filename, 50)
    print(f"Test2 got {test2}, expected {test2_expected}")
    assert test2 == test2_expected

    puzz2 = partx(puzzle_filename, 50)
    print(f"Puzzle2 is {puzz2}")
