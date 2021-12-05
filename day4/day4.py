# --- Day 4: Giant Squid ---

# You're already almost 1.5km (almost a mile) below the surface of the ocean,
# already so deep that you can't see any sunlight. What you can see, however,
# is a giant squid that has attached itself to the outside of your submarine.

# Maybe it wants to play bingo?

# Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
# Numbers are chosen at random, and the chosen number is marked on all boards
# on which it appears. (Numbers may not appear on all boards.) If all numbers
# in any row or any column of a board are marked, that board wins.
# (Diagonals don't count.)

# The submarine has a bingo subsystem to help passengers (currently, you and
# the giant squid) pass the time. It automatically generates a random order in
# which to draw numbers and a random set of boards (your puzzle input). For
# example:

# 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

# 22 13 17 11  0
#  8  2 23  4 24
# 21  9 14 16  7
#  6 10  3 18  5
#  1 12 20 15 19

#  3 15  0  2 22
#  9 18 13 17  5
# 19  8  7 25 23
# 20 11 10 24  4
# 14 21 16 12  6

# 14 21 17 24  4
# 10 16 15  9 19
# 18  8 23 26 20
# 22 11 13  6  5
#  2  0 12  3  7

# After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
# winners, but the boards are marked as follows (shown here adjacent to each
# other to save space):

# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

# After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are
# still no winners:

# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

# Finally, 24 is drawn:

# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

# At this point, the third board wins because it has at least one complete
# row or column of marked numbers (in this case, the entire top row is
# marked: 14 21 17 24 4).

# The score of the winning board can now be calculated. Start by finding the
# sum of all unmarked numbers on that board; in this case, the sum is 188.
# Then, multiply that sum by the number that was just called when the board
# won, 24, to get the final score, 188 * 24 = 4512.

# To guarantee victory against the giant squid, figure out which board will win
# first. What will your final score be if you choose that board?
#


# THINKING: this is a sets problem, cool. Each board object needs to be able to
#  understand if it won based on the list of numbers called so far.
#  is also needs to be able to score itself based on those numbers
#

# Your puzzle answer was 38913.
# --- Part Two ---

# On the other hand, it might be wise to try a different strategy: let the
# giant squid win.

# You aren't sure how many bingo boards a giant squid could play at once, so
# rather than waste time counting its arms, the safe thing to do is to figure
# out which board will win last and choose that one. That way, no matter which
# boards it picks, it will win for sure.

# In the above example, the second board is the last to win, which happens
# after 13 is eventually called and its middle column is completely marked. If
# you were to keep playing until this point, the second board would have a sum
# of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

# Figure out which board will win last. Once it wins, what would its final
# score be?

# Your puzzle answer was 16836.


from typing import List


class BingoCard:
    def __init__(self, numbers: List) -> None:
        # The numbers iterable must be 25 ints..
        assert len(numbers) == 25
        self.all_numbers = set(numbers)
        self.lines = []
        for i in range(5):
            # Create a horizontal set..
            self.lines.append(set(numbers[5 * i : 5 * i + 5]))
            # And a vertical set..
            the_list = [numbers[i + 5 * row] for row in range(5)]
            self.lines.append(set(the_list))

    def __repr__(self) -> str:
        result: str = ""
        result = f"BingoBoard<{self.all_numbers}> ({self.lines})"
        return result

    def is_bingo(self, called_numbers_list: List[int]) -> bool:
        """
        Return True if this card has a bingo
        """
        bingo = False
        idx = 0
        while not bingo and idx < len(self.lines):
            # Check this one
            if self.lines[idx].issubset(called_numbers_list):
                bingo = True

            # move onto the next one
            idx += 1
        return bingo

    def score_card(self, called_numbers_list: List[int]) -> int:
        """
        Return the score for the card, which is to say all
        the numbers which do not appear in the called number list
        multiplied by the last number called
        """
        uncalled = self.all_numbers.difference(called_numbers_list)
        unmarked_total = sum(uncalled)
        score = called_numbers_list[-1] * unmarked_total
        return score


class BingoGame:
    called_numbers = None
    boards = None

    def __init__(self) -> None:
        self.boards = []

    def summary(self):
        print(
            f"BingoGame: called_numbers={len(self.called_numbers)}, board_count={len(self.boards)}"
        )

    def load_bingo_game(self, filename: str):
        """
        Load a bingo game setup from a file
        """
        with open(filename, "r") as f:
            # digits so far..
            stored_digits = []
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # actual line to process..
                    # is it the first line with commas ?
                    if "," in this_line:
                        line_parts = this_line.split(",")
                    else:
                        line_parts = this_line.split(" ")
                    line_values = [int(x) for x in line_parts if x != ""]
                    # now decide what to do with this..
                    if self.called_numbers is None:
                        self.called_numbers = line_values
                    else:
                        # ok, we got some numbers, but do we have enough for a card ?
                        stored_digits.extend(line_values)
                        if 25 == len(stored_digits):
                            # got a new card..
                            the_card = BingoCard(stored_digits)
                            self.boards.append(the_card)
                            stored_digits = []

    def __repr__(self) -> str:
        result = f"BingoGame\nCalled: {self.called_numbers}\nBoard Count: {len(self.boards)}\n"
        for b in self.boards:
            result += f"{b}\n"
        return result

    def find_winning_board(self):
        """
        Determine the score for the winning board
        """
        count = 5
        bingo = False

        while not bingo:
            # Get the called numbers list so far
            already_called = self.called_numbers[:count]
            # check to see if any boards have a bingo here..
            for this_board in self.boards:
                if this_board.is_bingo(already_called):
                    bingo = True
                    score = this_board.score_card(already_called)
            # next number then..
            count += 1

        return score

    def find_losing_board(self):
        """
        Determine the score for the last board to complete
        """
        count = 5

        remaining_boards = self.boards.copy()

        while len(remaining_boards) > 0:
            # Get the called numbers list so far
            already_called = self.called_numbers[:count]
            print(f"Starting to loop with {len(remaining_boards)} and {already_called}")
            # check to see if any boards have a bingo here, if they do, remove them
            for idx in range(len(remaining_boards) - 1, -1, -1):
                this_board = remaining_boards[idx]
                if this_board.is_bingo(already_called):
                    print(f"Removing board at #{idx}")
                    # remove this one..
                    del remaining_boards[idx]
                    # if this was the last one, then this is the answer..
                    score = this_board.score_card(already_called)

            # next number then..
            count += 1

        return score


def part1(filename: str) -> int:
    """
    Run the part1 logic..
    """
    game = BingoGame()
    game.load_bingo_game(filename)
    game.summary()
    score = game.find_winning_board()
    print(f"Winning score is : {score}")
    return score


def part2(filename: str) -> int:
    """
    Run the part2 logic..
    """
    game = BingoGame()
    game.load_bingo_game(filename)
    game.summary()
    score = game.find_losing_board()
    print(f"Losing score is : {score}")
    return score


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"

    test_result = part1(test_filename)
    assert 4512 == test_result

    part1_result = part1(puzzle_filename)
    print(f"Part 1 result is {part1_result}")

    part2_test = part2(test_filename)
    print(f"Part 2 test result is {part2_test}")
    assert 1924 == part2_test

    part2_result = part2(puzzle_filename)
    print(f"Part 2 result is {part2_result}")
