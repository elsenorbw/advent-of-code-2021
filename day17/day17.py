# --- Day 17: Trick Shot ---

# You finally decode the Elves' message. HI, the message says. You continue
# searching for the sleigh keys.

# Ahead of you is what appears to be a large ocean trench. Could the keys have
# fallen into it? You'd better send a probe to investigate.

# The probe launcher on your submarine can fire the probe with any integer
# velocity in the x (forward) and y (upward, or downward if negative)
# directions. For example, an initial x,y velocity like 0,10 would fire the
# probe straight up, while an initial velocity like 10,-1 would fire the probe
# forward at a slight downward angle.

# The probe's x,y position starts at 0,0. Then, it will follow some trajectory
# by moving in steps. On each step, these changes occur in the following order:

#     The probe's x position increases by its x velocity.
#     The probe's y position increases by its y velocity.
#     Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
#     Due to gravity, the probe's y velocity decreases by 1.

# For the probe to successfully make it into the trench, the probe must be on
# some trajectory that causes it to be within a target area after any step.
# The submarine computer has already calculated this target area
# (your puzzle input). For example:

# target area: x=20..30, y=-10..-5

# This target area means that you need to find initial x,y velocity values such
# that after any step, the probe's x position is at least 20 and at most 30,
# and the probe's y position is at least -10 and at most -5.

# Given this target area, one initial velocity that causes the probe to be
# within the target area after any step is 7,2:

# .............#....#............
# .......#..............#........
# ...............................
# S........................#.....
# ...............................
# ...............................
# ...........................#...
# ...............................
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTT#TT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT

# In this diagram, S is the probe's initial position, 0,0. The x coordinate
# ncreases to the right, and the y coordinate increases upward.
# In the bottom right, positions that are within the target area are shown as T
# After each step (until the target area is reached), the position of the probe
# is marked with #. (The bottom-right # is both a position the probe reaches
# and a position in the target area.)

# Another initial velocity that causes the probe to be within the target area
# after any step is 6,3:

# ...............#..#............
# ...........#........#..........
# ...............................
# ......#..............#.........
# ...............................
# ...............................
# S....................#.........
# ...............................
# ...............................
# ...............................
# .....................#.........
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................T#TTTTTTTTT
# ....................TTTTTTTTTTT

# Another one is 9,0:

# S........#.....................
# .................#.............
# ...............................
# ........................#......
# ...............................
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTT#
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT
# ....................TTTTTTTTTTT

# One initial velocity that doesn't cause the probe to be within the target
# area after any step is 17,-4:

# S..............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# .................#.............................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT................................
# ....................TTTTTTTTTTT..#.............................
# ....................TTTTTTTTTTT................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ................................................#..............
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ...............................................................
# ..............................................................#

# The probe appears to pass through the target area, but is never within it
# after any step. Instead, it continues down and to the right - only the first
# few steps are shown.

# If you're going to fire a highly scientific probe out of a super cool probe
# launcher, you might as well do it with style. How high can you make the probe
# go while still reaching the target area?

# In the above example, using an initial velocity of 6,9 is the best you can
# do, causing the probe to reach a maximum y position of 45. (Any higher
# initial y velocity causes the probe to overshoot the target area entirely.)

# Find the initial velocity that causes the probe to reach the highest y
# position and still eventually be within the target area after any step.
# What is the highest y position it reaches on this trajectory?


# THINKING: The real question here is the Y velocity, the X is irrelevant to
# the question as it just keeps slowing down so some X velocity with get us
# to stop in the zone.

# so any given upwards launch has a height where the y velocity becomes 0
# this point must be the apex, and from the apex we start to drop at a steady
# gravity rate. Let's start by calculating all the apex positions. Since we're
# looking for highest, propose starting with 1.

# So - anything that goes up with velocity X must arrive back at zero with velocity 0 - (X + 1)
# e.g. launching with 17 will get back to 0 with -18 velocity for the next step
# since the logically largest speed downwards will plummet to the last line of the zone
# in the next step, the lower of the y co-ordinates will be the target depth for the next step..


def apex_for(velocity: int, start_height: int = 0) -> int:
    """
    Calculate the apex for a given start height
    """
    result = start_height
    while velocity > 0:
        result += velocity
        velocity -= 1
    return result


def inside_grid(x, y, x1, x2, y1, y2):
    result = False
    if x >= min(x1, x2) and x <= max(x1, x2) and y >= min(y1, y2) and y <= max(y1, y2):
        result = True
    return result


def hits_area(x_velocity: int, y_velocity: int, x1: int, x2: int, y1: int, y2: int):
    """
    Will a launch starting at 0, 0 given these parameters hit the target area ?
    """
    x = 0
    y = 0
    grid_bottom = min(y1, y2)
    while y > grid_bottom:
        # make a move..
        x += x_velocity
        y += y_velocity
        # adjust next velocity - assuming positive x values
        x_velocity = max(0, x_velocity - 1)
        y_velocity -= 1
        # are we in the grid ?
        if inside_grid(x, y, x1, x2, y1, y2):
            return True
    return False


def information():
    for velocity in range(42):
        print(f"Velocity {velocity}, apex={apex_for(velocity)}")


def part1(x1: int, x2: int, y1: int, y2: int):
    """
    Calculate the apex of the largest velocity that will still hit the zone
    """
    bottom_y = min(y1, y2)
    assert bottom_y < 0
    start_velocity = 0 - bottom_y - 1
    apex = apex_for(start_velocity)
    return apex


def part2(x1: int, x2: int, y1: int, y2: int):
    """
    Figure out how many potential launch combinations end in the target zone
    """
    combinations = []
    for this_x_velocity in range(1, max(x1, x2) + 1):
        bottom_y = min(y1, y2)
        max_start_y_velocity = 0 - bottom_y - 1
        for this_y_velocity in range(min(y1, y2), max_start_y_velocity + 1):
            if hits_area(this_x_velocity, this_y_velocity, x1, x2, y1, y2):
                combinations.append((this_x_velocity, this_y_velocity))
                print(f"Found a matching velocity {this_x_velocity},{this_y_velocity}")
    return len(combinations)


if __name__ == "__main__":
    information()
    # x=20..30, y=-10..-5
    test_input = (20, 30, -10, -5)
    expected1 = 45
    expected2 = 112

    # x=281..311, y=-74..-54
    puzzle_input = (281, 311, -74, -54)

    test1 = part1(*test_input)
    print(f"test1 got {test1}, expected {expected1}")
    assert expected1 == test1

    puzz1 = part1(*puzzle_input)
    print(f"puzz1 got {puzz1}")

    test2 = part2(*test_input)
    print(f"test2 for {test2}, expected {expected2}")
    assert test2 == expected2

    puzz2 = part2(*puzzle_input)
    print(f"Puzzle part 2 got {puzz2}")
