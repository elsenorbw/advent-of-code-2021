# --- Day 7: The Treachery of Whales ---

# A giant whale has decided your submarine is its next meal, and it's much
# faster than you are. There's nowhere to run!

# Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep
# for them otherwise) zooms in to rescue you! They seem to be preparing to
# blast a hole in the ocean floor; sensors indicate a massive underground cave
# system just beyond where they're aiming!

# The crab submarines all need to be aligned before they'll have enough power
# to blast a large enough hole for your submarine to get through. However, it
# doesn't look like they'll be aligned before the whale catches you! Maybe you
# can help?

# There's one major catch - crab submarines can only move horizontally.

# You quickly make a list of the horizontal position of each crab (your puzzle
# input). Crab submarines have limited fuel, so you need to find a way to make
# all of their horizontal positions match while requiring them to spend as
# little fuel as possible.

# For example, consider the following horizontal positions:

# 16,1,2,0,4,2,7,1,2,14

# This means there's a crab with horizontal position 16, a crab with horizontal
# position 1, and so on.

# Each change of 1 step in horizontal position of a single crab costs 1 fuel.
# You could choose any horizontal position to align them all on, but the one
# that costs the least fuel is horizontal position 2:

#     Move from 16 to 2: 14 fuel
#     Move from 1 to 2: 1 fuel
#     Move from 2 to 2: 0 fuel
#     Move from 0 to 2: 2 fuel
#     Move from 4 to 2: 2 fuel
#     Move from 2 to 2: 0 fuel
#     Move from 7 to 2: 5 fuel
#     Move from 1 to 2: 1 fuel
#     Move from 2 to 2: 0 fuel
#     Move from 14 to 2: 12 fuel

# This costs a total of 37 fuel. This is the cheapest possible outcome; more
# expensive outcomes include aligning at position 1 (41 fuel),
# position 3 (39 fuel), or position 10 (71 fuel).

# Determine the horizontal position that the crabs can align to using the least
# fuel possible. How much fuel must they spend to align to that position?

#
#  THINKING: Tricky one, the answer might be the median value, we might be able
#            to binary split the values and walk towards the answer *if* it is
#            true that moving away from the answer always makes the score worse
#            it seems like that should be true but unclear on that one.
#            going to start with the full mathy option..
#
#            Also, could obviously just brute force it, but that seems lazy.


# --- Part Two ---

# The crabs don't seem interested in your proposed solution. Perhaps you
# misunderstand crab engineering?

# As it turns out, crab submarine engines don't burn fuel at a constant rate.
# Instead, each change of 1 step in horizontal position costs 1 more unit of
# fuel than the last: the first step costs 1, the second step costs 2, the
# third step costs 3, and so on.

# As each crab moves, moving further becomes more expensive. This changes the
# best horizontal position to align them all on; in the example above, this
# becomes 5:

#     Move from 16 to 5: 66 fuel
#     Move from 1 to 5: 10 fuel
#     Move from 2 to 5: 6 fuel
#     Move from 0 to 5: 15 fuel
#     Move from 4 to 5: 1 fuel
#     Move from 2 to 5: 6 fuel
#     Move from 7 to 5: 3 fuel
#     Move from 1 to 5: 10 fuel
#     Move from 2 to 5: 6 fuel
#     Move from 14 to 5: 45 fuel

# This costs a total of 168 fuel. This is the new cheapest possible outcome;
# the old alignment position (2) now costs 206 fuel instead.

# Determine the horizontal position that the crabs can align to using the
# least fuel possible so they can make you an escape route! How much fuel must
# they spend to align to that position?


from typing import List, Match
import statistics


def load_csv_int_list(filename: str) -> List[int]:
    """
    Read a file full of csv separated int values and
    return a single list of all of them in order
    """
    all_values: List[int] = []
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                these_values = [int(x) for x in this_line.split(",") if x != ""]
                all_values.extend(these_values)
    return all_values


def crab_fuel_expense(crabs: List[int], destination: int) -> int:
    """
    What is the total fuel required for these crabs to get to
    the specified destination
    """
    result = sum([abs(destination - this_pos) for this_pos in crabs])
    return result


def triangle_number(n: int) -> int:
    """
    Return the nth triangular number for this
    """
    result = int(n * (n + 1) / 2)
    return result


def crab_fuel_expense_two(crabs: List[int], destination: int) -> int:
    """
    What is the total fuel required for these crabs to get to
    the specified destination
    In this case each step is one more than the previous..
    so...
    1=1
    2=3
    3=6
    4=10
    5=15
    So this is a triangular number.. so the calculation is :
    triangle for n = n * (n + 1) / 2
    1 == 1 * 2 / 2 -> yep
    3 == 2 * 3 / 2 -> yep
    5 == 5 * 6 / 2 -> yep..
    ok.. sold..
    """
    result = sum([triangle_number(abs(destination - this_pos)) for this_pos in crabs])
    return result


def brute_force_solve(crabs: List[int]) -> int:
    """
    Find the best position and return the position and the score
    """
    small_crab = min(crabs)
    big_crab = max(crabs)

    best_score = 900000000
    best_pos = -1

    all_scores = []

    for this_position in range(small_crab, big_crab + 1):
        # what is this score..
        score = crab_fuel_expense(crabs, this_position)
        all_scores.append(score)
        if score < best_score:
            best_score = score
            best_pos = this_position

    print(f"Best position: {best_pos} with a score of {best_score}")
    print(f"All Scores: {all_scores}")
    return best_pos, best_score


def brute_force_solve_two(crabs: List[int]) -> int:
    """
    Find the best position and return the position and the score
    """
    small_crab = min(crabs)
    big_crab = max(crabs)

    best_score = 900000000
    best_pos = -1

    all_scores = []

    for this_position in range(small_crab, big_crab + 1):
        # what is this score..
        score = crab_fuel_expense_two(crabs, this_position)
        all_scores.append(score)
        if score < best_score:
            best_score = score
            best_pos = this_position

    print(f"Best position: {best_pos} with a score of {best_score}")
    print(f"All Scores: {all_scores}")
    return best_pos, best_score


def part1(filename: str) -> int:
    """
    Solve part1
    """
    crab_positions = load_csv_int_list(filename)

    # determine the best position
    brute_pos, brute_score = brute_force_solve(crab_positions)
    print(
        f"Averages: mode={statistics.mode(crab_positions)} median={statistics.median(crab_positions)} mean={statistics.mean(crab_positions)}"
    )

    return brute_score


def part2(filename: str) -> int:
    """
    Solve part1
    """
    crab_positions = load_csv_int_list(filename)

    # determine the best position
    brute_pos, brute_score = brute_force_solve_two(crab_positions)
    return brute_score


if __name__ == "__main__":
    test_filename = "test_input.txt"
    test_part1_expected_result = 37
    puzzle_filename = "puzzle_input.txt"
    test_part1 = part1(test_filename)
    print(f"Part1 test result is {test_part1} (should be {test_part1_expected_result})")
    assert test_part1 == test_part1_expected_result
    part1_result = part1(puzzle_filename)
    print(f"Part1 actual result is {part1_result}")

    test_part2 = part2(test_filename)
    test_part2_expected_result = 168
    print(f"Part2 test result is {test_part2} (should be {test_part2_expected_result})")
    assert test_part2 == test_part2_expected_result
    part2_result = part2(puzzle_filename)
    print(f"Part2 actual result is {part2_result}")
