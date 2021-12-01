# --- Day 1: Sonar Sweep ---

# You're minding your own business on a ship at sea when the overboard alarm
# goes off! You rush to see if you can help. Apparently, one of the Elves
# tripped and accidentally sent the sleigh keys flying into the ocean!

# Before you know it, you're inside a submarine the Elves keep ready for
# situations like this. It's covered in Christmas lights (because of course
# it is), and it even has an experimental antenna that should be able to track
# the keys if you can boost its signal strength high enough; there's a little
# meter that indicates the antenna's signal strength by displaying 0-50 stars.

# Your instincts tell you that in order to save Christmas, you'll need to get
# all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each
# day in the Advent calendar; the second puzzle is unlocked when you complete
# the first. Each puzzle grants one star. Good luck!

# As the submarine drops below the surface of the ocean, it automatically
# performs a sonar sweep of the nearby sea floor. On a small screen, the sonar
# sweep report (your puzzle input) appears: each line is a measurement of the
# sea floor depth as the sweep looks further and further away from the
# submarine.

# For example, suppose you had the following report:

# 199
# 200
# 208
# 210
# 200
# 207
# 240
# 269
# 260
# 263

# This report indicates that, scanning outward from the submarine, the sonar
# sweep found depths of 199, 200, 208, 210, and so on.

# The first order of business is to figure out how quickly the depth increases,
# just so you know what you're dealing with - you never know if the keys will
# get carried into deeper water by an ocean current or a fish or something.

# To do this, count the number of times a depth measurement increases from the
# previous measurement. (There is no measurement before the first measurement.)
# In the example above, the changes are as follows:

# 199 (N/A - no previous measurement)
# 200 (increased)
# 208 (increased)
# 210 (increased)
# 200 (decreased)
# 207 (increased)
# 240 (increased)
# 269 (increased)
# 260 (decreased)
# 263 (increased)

# In this example, there are 7 measurements that are larger than the previous
# measurement.

# How many measurements are larger than the previous measurement?

from typing import List


def count_increases(list_of_depths: List[int]) -> int:
    """
    For each value in the input list, if it is larger than the previous one
    add one to the total, returning that total as the result.
    """
    result = 0

    bigger_than_previous = [
        1 if list_of_depths[i] > list_of_depths[i - 1] else 0
        for i in range(1, len(list_of_depths))
    ]

    result = sum(bigger_than_previous)

    return result


def load_integers_from_file(filename: str) -> List[int]:
    """
    Given a filename, load that file and parse each line as an int.
    return the contents as a list of int.
    """
    result: List[int] = []

    with open(filename, "r") as f:
        for this_line in f:
            # remove the whitespace
            this_line = this_line.strip()
            # get an integer..
            this_int = int(this_line)
            # and stuff it into the result.
            result.append(this_int)

    return result


def part1(filename):
    the_list = load_integers_from_file(filename)
    result = count_increases(the_list)
    return result


if __name__ == "__main__":
    test_filename = "test_input.txt"
    test_answer = part1(test_filename)
    assert 7 == test_answer
    filename = "puzzle_input.txt"
    answer = part1(filename)
    print(f"The answer for part1 is {answer}")
