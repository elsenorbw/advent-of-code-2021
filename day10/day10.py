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

# --- Part Two ---

# Now, discard the corrupted lines. The remaining lines are incomplete.

# Incomplete lines don't have any incorrect characters - instead, they're
# missing some closing characters at the end of the line. To repair the
# navigation subsystem, you just need to figure out the sequence of closing
# characters that complete all open chunks in the line.

# You can only use closing characters (), ], }, or >), and you must add them in
# the correct order so that only legal pairs are formed and all chunks end up
# closed.

# In the example above, there are five incomplete lines:

#     [({(<(())[]>[[{[]{<()<>> - Complete by adding }}]])})].
#     [(()[<>])]({[<{<<[]>>( - Complete by adding )}>]}).
#     (((({<>}<{<{<>}{[]{[]{} - Complete by adding }}>}>)))).
#     {<[[]]>}<{[{[{[]{()[[[] - Complete by adding ]]}}]}]}>.
#     <{([{{}}[<[[[<>{}]]]>[]] - Complete by adding ])}>.

# Did you know that autocomplete tools also have contests? It's true! The
# score is determined by considering the completion string
# character-by-character. Start with a total score of 0. Then, for each
# character, multiply the total score by 5 and then increase the total score
# by the point value given for the character in the following table:

#     ): 1 point.
#     ]: 2 points.
#     }: 3 points.
#     >: 4 points.

# So, the last completion string above - ])}> - would be scored as follows:

#     Start with a total score of 0.
#     Multiply the total score by 5 to get 0, then add the value of ] (2) to get a new total score of 2.
#     Multiply the total score by 5 to get 10, then add the value of ) (1) to get a new total score of 11.
#     Multiply the total score by 5 to get 55, then add the value of } (3) to get a new total score of 58.
#     Multiply the total score by 5 to get 290, then add the value of > (4) to get a new total score of 294.

# The five lines' completion strings have total scores as follows:

#     }}]])})] - 288957 total points.
#     )}>]}) - 5566 total points.
#     }}>}>)))) - 1480781 total points.
#     ]]}}]}]}> - 995444 total points.
#     ])}> - 294 total points.

# Autocomplete tools are an odd bunch: the winner is found by sorting all of
# the scores and then taking the middle score. (There will always be an odd
# number of scores to consider.) In this example, the middle score is 288957
# because there are the same number of scores smaller and larger than it.

# Find the completion string for each incomplete line, score the completion
# strings, and sort the scores. What is the middle score?


from typing import Optional


def is_opener(s: str) -> bool:
    return s in "({<["


def is_closer(s: str) -> bool:
    return s in ")}>]"


def matched_closers(opener: str, closer: str) -> bool:
    acceptable_pairs = [("{", "}"), ("(", ")"), ("<", ">"), ("[", "]")]
    this_pair = (opener, closer)
    return this_pair in acceptable_pairs


def closer_for(opener: str) -> str:
    closers = {"{": "}", "(": ")", "<": ">", "[": "]"}
    return closers[opener]


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


def get_closing_brackets_required(s: str) -> Optional[str]:
    """
    Return the string of closing brackets required or None for broken lines
    """
    the_stack = []
    for this_char in s:
        if is_opener(this_char):
            the_stack.append(this_char)
        elif is_closer(this_char):
            top_item = the_stack.pop()
            if not matched_closers(top_item, this_char):
                # got it..
                return None
        else:
            # What the actual hell ?
            print(f"This thing ->{this_char} is not an opener nor a closer..")
            exit(1)

    # ok, we have a string, let's create the answer..
    print(f"Need to close {the_stack}")
    answer = []
    while len(the_stack) > 0:
        this_one = the_stack.pop()
        answer.append(closer_for(this_one))

    print(f"  Closed with {answer}")

    return answer


def get_closing_score(s: str) -> int:
    """
    Use the weird rules to score this...

    ): 1 point.
    ]: 2 points.
    }: 3 points.
    >: 4 points.

    """
    the_scores = {")": 1, "]": 2, "}": 3, ">": 4}

    score = 0
    for this_closer in s:
        score *= 5
        score += the_scores[this_closer]
    return score


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


def part2(filename: str) -> int:
    """
    For each line with no incorrect bracket,
      determine that required closing brackets
      score that closure using the (current * 5) + score(x) rule
      put that score in the list of all scores
    sort the list and return the middle value
    """
    all_scores = []

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                this_missing_bit = get_closing_brackets_required(this_line)
                if this_missing_bit is not None:
                    this_score = get_closing_score(this_missing_bit)
                    all_scores.append(this_score)
    print(all_scores)

    sorted_scores = sorted(all_scores)
    idx = int(len(sorted_scores) / 2)
    print(
        f"scores has {len(sorted_scores)} items, picking index {idx} which is {sorted_scores[idx]}"
    )
    result = sorted_scores[idx]
    return result


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test_part1_expected_result = 26397
    test_part2_expected_result = 288957

    test1 = part1(test_filename)
    print(f"test1 result is {test1} - should be {test_part1_expected_result}")
    assert test1 == test_part1_expected_result

    puzz1 = part1(puzzle_filename)
    print(f"part1 is {puzz1}")

    test2 = part2(test_filename)
    print(f"test2 result is {test2} - should be {test_part2_expected_result}")
    assert test2 == test_part2_expected_result

    puzz2 = part2(puzzle_filename)
    print(f"part2 is {puzz2}")
