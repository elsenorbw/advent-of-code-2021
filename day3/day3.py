# --- Day 3: Binary Diagnostic ---

# The submarine has been making some odd creaking noises, so you ask it to
# produce a diagnostic report just in case.

# The diagnostic report (your puzzle input) consists of a list of binary
# numbers which, when decoded properly, can tell you many useful things about
# the conditions of the submarine. The first parameter to check is the power
# consumption.

# You need to use the binary numbers in the diagnostic report to generate two
# new binary numbers (called the gamma rate and the epsilon rate). The power
# consumption can then be found by multiplying the gamma rate by the
# epsilon rate.

# Each bit in the gamma rate can be determined by finding the most common bit
# in the corresponding position of all numbers in the diagnostic report. For
# example, given the following diagnostic report:

# 00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010

# Considering only the first bit of each number, there are five 0 bits and
# seven 1 bits. Since the most common bit is 1, the first bit of the gamma
# rate is 1.

# The most common second bit of the numbers in the diagnostic report is 0,
# so the second bit of the gamma rate is 0.

# The most common value of the third, fourth, and fifth bits are 1, 1, and 0,
# respectively, and so the final three bits of the gamma rate are 110.

# So, the gamma rate is the binary number 10110, or 22 in decimal.

# The epsilon rate is calculated in a similar way; rather than use the most
# common bit, the least common bit from each position is used. So, the epsilon
# rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the
# epsilon rate (9) produces the power consumption, 198.

# Use the binary numbers in your diagnostic report to calculate the gamma rate
# and epsilon rate, then multiply them together. What is the power consumption
# of the submarine? (Be sure to represent your answer in decimal, not binary.)


#
# Thinking: ok, looks like fun. This is going to be easier as strings initially
# and then we can convert it to binary at the end to get the values
#

# Your puzzle answer was 4139586.

# The first half of this puzzle is complete! It provides one gold star: *
# --- Part Two ---

# Next, you should verify the life support rating, which can be determined by
# multiplying the oxygen generator rating by the CO2 scrubber rating.

# Both the oxygen generator rating and the CO2 scrubber rating are values that
# can be found in your diagnostic report - finding them is the tricky part.
# Both values are located using a similar process that involves filtering out
# values until only one remains. Before searching for either rating value,
# start with the full list of binary numbers from your diagnostic report and
# consider just the first bit of those numbers. Then:

#     Keep only numbers selected by the bit criteria for the type of rating
#       value for which you are searching. Discard numbers which do not match
#       the bit criteria.
#     If you only have one number left, stop; this is the rating value for
#       which you are searching.
#     Otherwise, repeat the process, considering the next bit to the right.

# The bit criteria depends on which type of rating value you want to find:

#     To find oxygen generator rating, determine the most common value (0 or 1)
#       in the current bit position, and keep only numbers with that bit in
#       that position. If 0 and 1 are equally common, keep values with a 1 in
#       the position being considered.
#     To find CO2 scrubber rating, determine the least common value (0 or 1) in
#       the current bit position, and keep only numbers with that bit in that
#       position. If 0 and 1 are equally common, keep values with a 0 in the
#       position being considered.

# For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

#     Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
#     Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
#     In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
#     In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
#     In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
#     As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

# Then, to determine the CO2 scrubber rating value from the same example above:

#     Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
#     Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
#     In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
#     As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.

# Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

# Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)


import math
from typing import List, Optional, Tuple


class DiagnosticReport:
    # A list of how many times we have seen each bit as a 1
    bit_counts: Optional[List[int]] = None
    # A list of the total number of values
    value_counts: int = 0
    # and store the individual bit strings as a list
    bit_strings: List[str] = []

    def __repr__(self) -> str:
        return f"({self.value_counts}) -> {self.bit_counts}"

    def add_one_bitstring(self, bitstring: str):
        """
        Given one "10101" style string, store it appropriately
        """
        # make sure we have a target array to fill in
        if self.bit_counts is None:
            self.bit_counts = [0 for _ in range(len(bitstring))]

        # add each digit
        for idx, bit in enumerate(bitstring):
            if "1" == bit:
                self.bit_counts[idx] += 1

        # and store the whole string
        self.bit_strings.append(bitstring)

        # and we have added one row
        self.value_counts += 1

    def load_file(self, filename: str):
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if this_line != "":
                    # we have a line to process
                    self.add_one_bitstring(this_line)
                    # and debug
                    # print(f"{this_line} {self}")

    def find_oxygen_scrubber(self):
        return self.filter_find(True, True)

    def find_co2_scrubber(self):
        return self.filter_find(False, False)

    def filter_find(self, find_most_common: bool, prefer_ones: bool) -> int:
        #
        #  find_most_common - set to True if we're looking for the ocygen generator case
        #                     set to False if we're looking for the CO2 scrubber
        #
        #  prefers_ones - what to do in the event of a tie, True for oxygen generator
        #                     False for CO2
        #
        # To find oxygen generator rating, determine the most common value (0 or 1)
        # in the current bit position, and keep only numbers with that bit in
        # that position. If 0 and 1 are equally common, keep values with a 1 in
        # the position being considered.
        #
        #  IMPORTANT NOTE: WE NEED TO CONSIDER WHAT IS MOST PREVALENT OF THE REMAINING SET
        #    EACH REDUCTION PASS, SO SOME SORT OF DIRTY LOOPING / RECURSION THING :)
        #
        result: int = -1
        candidates = self.bit_strings.copy()
        target_bit_index = 0

        while len(candidates) > 1:
            print(f"Starting candidate filter with {len(candidates)} candidates")
            #
            #  Whittle the list down a bit more.. (bit, get it?)
            #
            ones = []
            zeroes = []

            # sort everything into either the ones or zeros pile
            for this_bitmask in candidates:
                the_bit = this_bitmask[target_bit_index]
                if "0" == the_bit:
                    zeroes.append(this_bitmask)
                elif "1" == the_bit:
                    ones.append(this_bitmask)
                else:
                    raise ValueError(
                        "What the hell kind of bit is {the_bit} from {this_bitmask} ?"
                    )

            # ok, we have both lists, which one do we need to keep ?
            if len(ones) > len(zeroes):
                if find_most_common:
                    candidates = ones
                else:
                    candidates = zeroes
            elif len(ones) < len(zeroes):
                if find_most_common:
                    candidates = zeroes
                else:
                    candidates = ones
            else:
                # we have even-stevens, dealers choice
                if prefer_ones:
                    candidates = ones
                else:
                    candidates = zeroes

            # and we need to look at the next bit
            target_bit_index += 1

        # and we have the final value
        final_value = candidates[0]
        result = 0
        for this_bit in final_value:
            result *= 2
            if "1" == this_bit:
                result += 1

        return result

    def calculate_gamma_epsilon_rates(self) -> Tuple[int, int]:
        """
        Calculate the Gamma ane Epsilon Rate -
        Taking the most popular bit from each position
        Get that number and turn it into decimal
        """
        gamma: int = 0
        epsilon: int = 0

        # decided on rounding up, unclear from the spec,
        # demo has no example of that
        limit = math.ceil(self.value_counts / 2)

        # greater than or equal to the limit
        for this_bit in self.bit_counts:
            # move everything up..
            gamma *= 2
            epsilon *= 2
            if this_bit >= limit:
                gamma += 1
            else:
                epsilon += 1

        return gamma, epsilon


def part1(filename: str):
    """
    Run part1 of the puzzle
    """
    report = DiagnosticReport()
    report.load_file(filename)
    gamma, epsilon = report.calculate_gamma_epsilon_rates()
    return gamma * epsilon


def part2(filename: str):
    report = DiagnosticReport()
    report.load_file(filename)
    oxygen = report.find_oxygen_scrubber()
    co2 = report.find_co2_scrubber()
    result = oxygen * co2
    print(f"Oxygen:{oxygen}, CO2:{co2}, result:{result}")
    return result


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_input = "puzzle_input.txt"

    # test_result = part1(test_filename)
    # print(f"Test Part 1 is {test_result}")
    # assert test_result == 198

    # part1_result = part1(puzzle_input)
    # print(f"Part1 result is {part1_result}")

    test_result = part2(test_filename)
    print(f"Part2 test result: {test_result}")
    assert 230 == test_result
    part2_result = part2(puzzle_input)
    print(f"Part2 actual result: {part2_result}")
