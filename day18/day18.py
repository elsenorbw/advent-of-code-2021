# --- Day 18: Snailfish ---

# You descend into the ocean trench and encounter some snailfish. They say they
# saw the sleigh keys! They'll even tell you which direction the keys went if
# you help one of the smaller snailfish with his math homework.

# Snailfish numbers aren't like regular numbers. Instead, every snailfish
# number is a pair - an ordered list of two elements. Each element of the pair
# can be either a regular number or another pair.

# Pairs are written as [x,y], where x and y are the elements within the pair.
# Here are some example snailfish numbers, one snailfish number per line:

# [1,2]
# [[1,2],3]
# [9,[8,7]]
# [[1,9],[8,5]]
# [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
# [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
# [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]

# This snailfish homework is about addition. To add two snailfish numbers, form
# a pair from the left and right parameters of the addition operator.
# For example, [1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].

# There's only one problem: snailfish numbers must always be reduced, and the
# process of adding two snailfish numbers can result in snailfish numbers that
# need to be reduced.

# To reduce a snailfish number, you must repeatedly do the first action in this
# list that applies to the snailfish number:

#     If any pair is nested inside four pairs, the leftmost such pair explodes.
#     If any regular number is 10 or greater, the leftmost such regular number splits.

# Once no action in the above list applies, the snailfish number is reduced.

# During reduction, at most one action applies, after which the process returns to the top of the list of actions. For example, if split produces a pair that meets the explode criteria, that pair explodes before other splits occur.

# To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.

# Here are some examples of a single explode action:

#     [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular number to its left, so it is not added to any regular number).
#     [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular number to its right, and so it is not added to any regular number).
#     [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
#     [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action).
#     [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].

# To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.

# Here is the process of finding the reduced result of [[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

# after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
# after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
# after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
# after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
# after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
# after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

# Once no reduce actions apply, the snailfish number that remains is the actual result of the addition operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]].

# The homework assignment involves adding up a list of snailfish numbers (your puzzle input). The snailfish numbers are each listed on a separate line. Add the first snailfish number and the second, then add that result and the third, then add that result and the fourth, and so on until all numbers in the list have been used once.

# For example, the final sum of this list is [[[[1,1],[2,2]],[3,3]],[4,4]]:

# [1,1]
# [2,2]
# [3,3]
# [4,4]

# The final sum of this list is [[[[3,0],[5,3]],[4,4]],[5,5]]:

# [1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]

# The final sum of this list is [[[[5,0],[7,4]],[5,5]],[6,6]]:

# [1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# [6,6]

# Here's a slightly larger example:

# [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
# [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
# [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
# [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
# [7,[5,[[3,8],[1,4]]]]
# [[2,[2,2]],[8,[8,1]]]
# [2,9]
# [1,[[[9,3],9],[[9,0],[0,7]]]]
# [[[5,[7,4]],7],1]
# [[[[4,2],2],6],[8,7]]

# The final sum [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] is found after adding up the above snailfish numbers:

#   [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
# + [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
# = [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

#   [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
# + [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
# = [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

#   [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
# + [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
# = [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

#   [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
# + [7,[5,[[3,8],[1,4]]]]
# = [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

#   [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
# + [[2,[2,2]],[8,[8,1]]]
# = [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

#   [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
# + [2,9]
# = [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

#   [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
# + [1,[[[9,3],9],[[9,0],[0,7]]]]
# = [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

#   [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
# + [[[5,[7,4]],7],1]
# = [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

#   [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
# + [[[[4,2],2],6],[8,7]]
# = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

# To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element. The magnitude of a regular number is just that number.

# For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of [1,9] is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of [[9,1],[1,9]] is 3*29 + 2*21 = 129.

# Here are a few more magnitude examples:

#     [[1,2],[[3,4],5]] becomes 143.
#     [[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
#     [[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
#     [[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
#     [[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
#     [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.

# So, given this example homework assignment:

# [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
# [[[5,[2,8]],4],[5,[[9,9],0]]]
# [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
# [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
# [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
# [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
# [[[[5,4],[7,7]],8],[[8,3],8]]
# [[9,3],[[9,9],[6,[4,9]]]]
# [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
# [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]

# The final sum is:

# [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]

# The magnitude of this final sum is 4140.

# Add up all of the snailfish numbers from the homework assignment in the order they appear. What is the magnitude of the final sum?


from typing import List


class SnailfishNumber:
    UNSET = 1001
    PAIR = 1002
    REGULAR = 1003

    def __init__(self) -> None:
        self.type = SnailfishNumber.UNSET
        self.parent = None
        self.value = None
        self.left = None
        self.right = None

    def set_value(self, the_value: int):
        """
        Create a node with the regular type
        """
        self.type = SnailfishNumber.REGULAR
        self.value = the_value
        self.left = None
        self.right = None

    def set_pair(self, lhs: object, rhs: object):
        """
        Create a node that's a pair type
        """
        self.type = SnailfishNumber.PAIR
        self.left = lhs
        lhs.parent = self
        self.right = rhs
        rhs.parent = self
        self.value = None

    def reduce(self):
        """
        Reduce this number following the rules:
        loop until no changes are made:
          if any pair is nested inside 4 pairs (i.e. has 4 parents) then it explodes, left first
          if any regular number is greater than 10 then it is split
        """
        while True:
            # try to explode something
            if self.explode():
                continue
            # try to split something..
            if self.split():
                continue
            #  guess we're done..
            break

    def parent_count(self):
        """
        How many parents do we have ?
        """
        result = 0
        node = self
        while node.parent is not None:
            node = node.parent
            result += 1

        return result

    def get_root(self):
        """
        Return the ultimate parent node
        """
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def list_numbers(self, target: list):
        """
        Add all the REGULAR parts to the target list
        """
        if self.type == SnailfishNumber.REGULAR:
            target.append(self)
        else:
            self.left.list_numbers(target)
            self.right.list_numbers(target)

    def explode(self) -> bool:
        """
        Try to explode this pair or any kids..
        """
        result = False
        if self.type == SnailfishNumber.PAIR:
            # is this nested deeply enough ?
            if self.parent_count() == 4:
                # we can explode..
                # logic check - we should have two regular kids here..
                if (
                    self.left.type != SnailfishNumber.REGULAR
                    or self.right.type != SnailfishNumber.REGULAR
                ):
                    raise RuntimeError(f"Trying to explode a non-simple pair {self}")
                # ok, we can run the explode logic..

                # there's probably a much smarter way to do this, but it's not immediately coming to mind..
                the_list = []
                self.get_root().list_numbers(the_list)

                # left number gets added to the next left-hand value
                node_index = the_list.index(self.left)
                if node_index > 0:
                    the_list[node_index - 1].value += self.left.value
                # right number gets added to the next parent right-hand regular number..
                node_index = the_list.index(self.right)
                if node_index < len(the_list) - 1:
                    the_list[node_index + 1].value += self.right.value

                # this node turns into a 0
                self.set_value(0)
                result = True
            else:
                # try to blow up the kids..
                result = self.left.explode() or self.right.explode()

        return result

    def split(self) -> bool:
        """
        Split the left-most number that's more than 9 into two even parts,
        Leftovers go on the right
        """
        result = False
        if self.type == SnailfishNumber.REGULAR:
            if self.value > 9:
                left_value = int(self.value / 2)
                right_value = self.value - left_value
                new_left = SnailfishNumber()
                new_left.set_value(left_value)
                new_right = SnailfishNumber()
                new_right.set_value(right_value)
                self.set_pair(new_left, new_right)
                result = True
        else:
            result = self.left.split() or self.right.split()

        return result

    def __repr__(self) -> str:
        result = ""
        if self.type == SnailfishNumber.REGULAR:
            result = str(self.value)
        elif self.type == SnailfishNumber.PAIR:
            result = f"[{self.left},{self.right}]"
        else:
            result = "???"
        return result

    def magnitude(self):
        """
        For a pair, 3*left+2*right,
        For a number, the number
        """
        if self.type == SnailfishNumber.REGULAR:
            return self.value
        else:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def add(number1: object, number2: object) -> object:
        """
        Return the result of an addition
        """
        result = SnailfishNumber()
        result.set_pair(number1, number2)
        # and now reduce
        result.reduce()
        # and we're done..
        return result

    def add_list(numbers: List[str]) -> object:
        """
        Add all the strings as SnailfishNumbers and return the answer
        """
        answer = None
        for this_number_str in numbers:
            this_number = SnailfishNumber.parse(this_number_str)
            if answer is None:
                answer = this_number
            else:
                answer = SnailfishNumber.add(answer, this_number)
        return answer

    def parse(s: str) -> object:
        """
        Parse an input string and return the SnailfishNumber result
        """
        if s[0] == "[":
            # find the mid-way comma
            bracket_count = 0
            for comma_position, this_char in enumerate(s[1:]):
                if "," == this_char and 0 == bracket_count:
                    # we're done, this is the one..
                    break
                elif "[" == this_char:
                    bracket_count += 1
                elif "]" == this_char:
                    bracket_count -= 1

            # the comma position is 1 indexed, need to adjust
            comma_position += 1

            # got a comma, split up the remainder of the string
            lhs = s[1:comma_position]
            rhs = s[comma_position + 1 : -1]
            result = SnailfishNumber()
            left = SnailfishNumber.parse(lhs)
            right = SnailfishNumber.parse(rhs)
            result.set_pair(left, right)
        else:
            result = SnailfishNumber()
            result.set_value(int(s))
        return result


def part1(filename: str):
    """
    Add up all the numbers in the file and return the magnitude
    """
    number_list = []
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                number_list.append(this_line)

    total = SnailfishNumber.add_list(number_list)
    return total.magnitude()


def part2(filename: str):
    """
    Find the largest magnitude for any single pair addition in the list provided.
    """
    number_list = []
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                number_list.append(this_line)

    best_magnitude = -99999
    for a in number_list:
        for b in number_list:
            if a != b:
                # if there are duplicates, and they are the best answer, then we'll be back here swearing later on..
                ax = SnailfishNumber.parse(a)
                bx = SnailfishNumber.parse(b)
                cx = SnailfishNumber.add(ax, bx)
                this_magnitude = cx.magnitude()
                if this_magnitude > best_magnitude:
                    best_magnitude = this_magnitude
                    print(f"Best so far: {best_magnitude}: {a} + {b} = {cx}")
    return best_magnitude


if __name__ == "__main__":

    filename = "puzzle_input.txt"
    puzz1 = part1(filename)
    print(f"Part1 is {puzz1}")

    puzz2 = part2(filename)
    print(f"Part2 is {puzz2}")
