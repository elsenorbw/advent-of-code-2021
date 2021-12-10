# --- Day 10: Syntax Scoring ---

# You ask the submarine to determine the best route out of the deep-sea cave,
# but it only replies:

# Syntax error in navigation subsystem on line: all of them

# All of them?! The damage is worse than you thought. You bring up a copy of
# the navigation subsystem (your puzzle input).

# The navigation subsystem syntax is made of several lines containing chunks.
# There are one or more chunks on each line, and chunks contain zero or more
# other chunks. Adjacent chunks are not separated by any delimiter; if one
# chunk stops, the next chunk (if any) can immediately start. Every chunk
# must open and close with one of four legal pairs of matching characters:

#     If a chunk opens with (, it must close with ).
#     If a chunk opens with [, it must close with ].
#     If a chunk opens with {, it must close with }.
#     If a chunk opens with <, it must close with >.

# So, () is a legal chunk that contains no other chunks, as is []. More
# complex but valid chunks include ([]), {()()()}, <([{}])>,
# [<>({}){}[([])<>]], and even (((((((((()))))))))).

# Some lines are incomplete, but others are corrupted. Find and discard the
# corrupted lines first.

# A corrupted line is one where a chunk closes with the wrong character - that
# is, where the characters it opens and closes with do not form one of the four
# legal pairs listed above.

# Examples of corrupted chunks include (], {()()()>, (((()))}, and
# <([]){()}[{}]). Such a chunk can appear anywhere within a line, and its
# presence causes the whole line to be considered corrupted.

# For example, consider the following navigation subsystem:

# [({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]

# Some of the lines aren't corrupted, just incomplete; you can ignore these
# lines for now. The remaining five lines are corrupted:

#     {([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
#     [[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
#     [{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
#     [<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
#     <{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.

# Stop at the first incorrect closing character on each corrupted line.

# Did you know that syntax checkers actually have contests to see who can get
# the high score for syntax errors in a file? It's true! To calculate the
# syntax error score for a line, take the first illegal character on the line
# and look it up in the following table:

#     ): 3 points.
#     ]: 57 points.
#     }: 1197 points.
#     >: 25137 points.

# In the above example, an illegal ) was found twice (2*3 = 6 points), an
# illegal ] was found once (57 points), an illegal } was found once
# (1197 points), and an illegal > was found once (25137 points). So, the
# total syntax error score for this file is 6+57+1197+25137 = 26397 points!

# Find the first illegal character in each corrupted line of the navigation
# subsystem. What is the total syntax error score for those errors?


from typing import Optional


def is_opener(s: str) -> bool:
    return s in "({<["


def is_closer(s: str) -> bool:
    return s in ")}>]"


def matched_closers(opener: str, closer: str) -> bool:
    acceptable_pairs = [("{", "}"), ("(", ")"), ("<", ">"), ("[", "]")]
    this_pair = (opener, closer)
    return this_pair in acceptable_pairs


def get_first_incorrect_bracket(s: str) -> Optional[str]:
    """
    Return the first character that doesn't make sense or None
    """
    the_stack = []
    for this_char in s:
        if is_opener(this_char):
            the_stack.append(this_char)
        elif is_closer(this_char):
            top_item = the_stack.pop()
            if not matched_closers(top_item, this_char):
                # got it..
                return this_char
        else:
            # What the actual hell ?
            print(f"This thing ->{this_char} is not an opener nor a closer..")
            exit(1)
    return None


def get_score(s: str) -> int:
    """
    Arbitrary points system for scoring syntax errors..
    """
    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    score = 0
    if s in scores:
        score = scores[s]
    return score


def part1(filename: str) -> int:
    """
    For each line with an incorrect bracket,
      determine that bracket, score it and add to the total
    return the total
    """
    total = 0

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                this_error = get_first_incorrect_bracket(this_line)
                this_score = get_score(this_error)
                print(f"**** {this_line} **** -> {this_error} -> {this_score}")
                total += this_score

    return total


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test_part1_expected_result = 26397

    test1 = part1(test_filename)
    print(f"test1 result is {test1} - should be {test_part1_expected_result}")
    assert test1 == test_part1_expected_result

    puzz1 = part1(puzzle_filename)
    print(f"part1 is {puzz1}")
