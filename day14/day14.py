# --- Day 14: Extended Polymerization ---

# The incredible pressures at this depth are starting to put a strain on your
# submarine. The submarine has polymerization equipment that would produce
# suitable materials to reinforce the submarine, and the nearby
# volcanically-active caves should even have the necessary input elements in
# sufficient quantities.

# The submarine manual contains instructions for finding the optimal polymer
# formula; specifically, it offers a polymer template and a list of pair
# insertion rules (your puzzle input). You just need to work out what polymer
# would result after repeating the pair insertion process a few times.

# For example:

# NNCB

# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C

# The first line is the polymer template - this is the starting point of the
# process.

# The following section defines the pair insertion rules. A rule like AB -> C
# means that when elements A and B are immediately adjacent, element C should
# be inserted between them. These insertions all happen simultaneously.

# So, starting with the polymer template NNCB, the first step simultaneously
# considers all three pairs:

#     The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and the second N.
#     The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.
#     The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

# Note that these pairs overlap: the second element of one pair is the first
# element of the next pair. Also, because all pairs are considered
# simultaneously, inserted elements are not considered to be part of a pair
# until the next step.

# After the first step of this process, the polymer becomes NCNBCHB.

# Here are the results of a few steps using the above rules:

# Template:     NNCB
# After step 1: NCNBCHB
# After step 2: NBCCNBBBCBHCB
# After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
# After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

# This polymer grows quickly. After step 5, it has length 97; After step 10, it
# has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H
# occurs 161 times, and N occurs 865 times; taking the quantity of the most
# common element (B, 1749) and subtracting the quantity of the least common
# element (H, 161) produces 1749 - 161 = 1588.

# Apply 10 steps of pair insertion to the polymer template and find the most
# and least common elements in the result. What do you get if you take the
# quantity of the most common element and subtract the quantity of the least
# common element?


# THINKING: bet part2 is run a ridiculous number of these.. but for now, the simple way


from typing import Dict, Tuple


class Melter:
    def __init__(self, rules) -> None:
        # this is byref, don't care, read-only here..
        self.rules = rules
        self.cache = dict()

    def dict_merge(a: Dict, b: Dict) -> Dict:
        result = a.copy()
        for key, value in b.items():
            if key in result:
                result[key] += value
            else:
                result[key] = value
        return result

    def dict_from_string(s: str) -> Dict:
        result = dict()
        for x in s:
            if x not in result:
                result[x] = 1
            else:
                result[x] += 1
        return result

    def cache_key(pair: str, depth: int) -> Tuple:
        return (pair, depth)

    def melt(self, the_pair: str, depth: int) -> Dict:
        """
        Melt a single pair X times.. and return the counts of all the elements involved
        """
        key = Melter.cache_key(the_pair, depth)
        if key in self.cache:
            # print(f"Using a cached result for {key}")
            result = self.cache[key]
        else:
            # we need to calculate it and cache the result, but this is nicely recursive
            this_level_answer = self.rules[the_pair]
            # do we need to go lower ?
            if depth > 1:
                left_pair = the_pair[0] + this_level_answer
                right_pair = this_level_answer + the_pair[1]
                lhs = self.melt(left_pair, depth - 1)
                rhs = self.melt(right_pair, depth - 1)
                # remember to lose the middle duplication..
                result = Melter.dict_merge(lhs, rhs)
                result[this_level_answer] -= 1
            else:
                result = Melter.dict_from_string(
                    the_pair[0] + this_level_answer + the_pair[1]
                )
            # cache that sucker for next time
            # print(f"Storing a cached result for {key}")
            self.cache[key] = result

        return result


class Polymer:
    def __init__(self) -> None:
        self.poly = ""
        self.rules = dict()

    def __repr__(self) -> str:
        return f"Polymer:{self.poly}"

    def load_file(self, filename: str):
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # got a line.. but what is it ?
                    if "->" in this_line:
                        # it's a rule
                        parts = this_line.split("->")
                        pair = parts[0].strip()
                        result = parts[1].strip()
                        self.rules[pair] = result
                    else:
                        # must be the polymer
                        self.poly = this_line

    def naive_step(self):
        """
        Produce the next evolution of the polymer
        """
        this_poly = self.poly
        current_length = len(this_poly)
        next_poly = ""
        for x in range(current_length - 1):
            key = this_poly[x : x + 2]
            new_bit = self.rules[key]
            next_poly += this_poly[x]
            next_poly += new_bit
        # and add the last character..
        next_poly += this_poly[-1]
        # and we're done..
        # print(f"{this_poly} -> {next_poly}")
        self.poly = next_poly

    def step(self):
        """
        Produce the next evolution of the polymer
        but faster..
        """
        this_poly = self.poly
        next_poly = []

        this_char = this_poly[0]
        for next_char in this_poly[1:]:
            key = this_char + next_char
            new_bit = self.rules[key]
            next_poly.append(this_char)
            next_poly.append(new_bit)
            # shuffle down
            this_char = next_char

        # and add the last character..
        next_poly.append(this_poly[-1])
        # and we're done..
        # print(f"{this_poly} -> {next_poly}")
        self.poly = "".join(next_poly)

    def one_small_step_for_man(self, desired_iterations: int):
        """
        The idea is that we can already tell how big the result needs to be
        We also know where each element should sit in that final array already
        so potentially we can pre-allocate the array (thus saving a bunch of messing around)
        and work through the loops to generate the values we need..

        It might also be that a clever linked list thing works just as well.

        Also worth considering that all the work to take AB down 40 levels can be copied and reproduced easily from a top level..
        Oooh.. can we re-use various parts of the pyramid when we get a starting pair and a remaining depth ?
        As we work a 40 depth of a single pair down we also get a 39 depth of 2 other pairs etc..
        at any given height we might be able to reuse that work.. liking that idea the most so far, going to try that.
        This might work better as a separate merging object, it needs persistence and the rules..

        And that was a neat idea, but actually we run out of memory very quickly, thinking we might need counts of the characters rather than storing the strings..
        """
        melter = Melter(self.rules)

        # lazy for loop is fine across the top level, an irrelevance
        start_length = len(self.poly)

        final_counts = dict()
        for x in range(start_length - 1):
            pair = self.poly[x : x + 2]
            print(f"Need to create the counts for {pair} at depth {desired_iterations}")
            these_counts = melter.melt(pair, desired_iterations)
            print(
                f"The counts for {pair} at depth {desired_iterations} is {these_counts}"
            )
            # add them to final counts..
            final_counts = Melter.dict_merge(final_counts, these_counts)

        # and we're done..
        return final_counts

    def element_counts(self):
        """
        Return a dictionary of elements and their frequencies
        """
        result = dict()

        for this_element in self.poly:
            if this_element not in result:
                result[this_element] = 1
            else:
                result[this_element] += 1

        return result


def partx(filename: str, iterations: int) -> int:
    poly = Polymer()
    poly.load_file(filename)
    print(poly)

    # do all the iterations in one go..
    elements = poly.one_small_step_for_man(iterations)

    print(elements)
    frequencies = elements.values()
    sorted_frequencies = tuple(sorted(frequencies))
    print(sorted_frequencies)
    smallest = sorted_frequencies[0]
    largest = sorted_frequencies[-1]

    # and the answer is most common - least common
    answer = largest - smallest

    return answer


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test1_expected = 1588
    test2_expected = 2188189693529

    test1 = partx(test_filename, 10)
    print(f"test part1 got {test1}, expected {test1_expected}")
    assert test1 == test1_expected

    puzz1 = partx(puzzle_filename, 10)
    print(f"puzzle part1 is {puzz1}")

    test2 = partx(test_filename, 40)
    print(f"test part2 got {test2}, expected {test2_expected}")
    assert test2 == test2_expected

    puzz2 = partx(puzzle_filename, 40)
    print(f"puzzle part2 is {puzz2} and should not be 5208377027191")
    assert 5208377027191 != puzz2
