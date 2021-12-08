#
#  Figure out how to figure out the riddle..
#


def valid_segment_patterns():
    """
    Return a list of the valid segment patterns
    Given a segment diagram like this :

     111
    6   2
    6   2
    6   2
     777
    5   3
    5   3
    5   3
     444

    The patterns are :
    0 -> 123456
    1 -> 23
    2 -> 12457
    3 -> 12347
    4 -> 2367
    5 -> 13467
    6 -> 134567
    7 -> 123
    8 -> 1234567
    9 -> 123467

    """
    return [
        "123456",
        "23",
        "12457",
        "12347",
        "2367",
        "13467",
        "134567",
        "123",
        "1234567",
        "123467",
    ]


def sort_string(s: str) -> str:
    return "".join(sorted(s))


def print_segment_possibilities(sp):
    """
    Print out the current possibilities
    """
    print(f"Segment possiblities:")
    for this_segment in range(1, 8):
        print(f"Segment {this_segment} could be {sorted(sp[this_segment])}")
    print("\n")


def handle_one_line(the_line: str):
    # let's get everything nicely into tokens..
    parts = the_line.split("|")
    left_tokens = [x for x in parts[0].split(" ") if x != ""]
    right_tokens = [x for x in parts[1].split(" ") if x != ""]
    all_tokens = left_tokens + right_tokens
    print(f"All the tokens : {all_tokens}")
    # let's order the characters in each one to make life easier..
    ordered_tokens = [sort_string(x) for x in all_tokens]
    print(f"        Sorted : {ordered_tokens}")

    # ok, at this point we have to start narrowing it down..
    # we have a list of valid patterns
    valid_segments = valid_segment_patterns()
    print(f"Valid Segments are : {valid_segments}")
    for this_segment in sorted(valid_segments, key=len):
        print(f" - {this_segment}")

    # we have a list of possibilities for each segment, currently those possibilities are limitless
    # arse, have gone 1 based, damn.
    segment_possibilities = [{"a", "b", "c", "d", "e", "f", "g"} for _ in range(8)]
    print_segment_possibilities(segment_possibilities)

    # oh.. so.. if we have a combination of values then there are limited possible patterns for those values..
    # for example, given no other knowledge if we have a abcd then it's the only 4 sized pattern,
    # so abcd are options for elements 2367 and are no longer options for anything else.
    #
    #  This is basically sudoku solving, which I also suck at :) so let's see how we go..

    for this_signal_pattern in sorted(ordered_tokens, key=len):
        this_signal_pattern_set = set([x for x in this_signal_pattern])
        print(f"Handling {this_signal_pattern} ({this_signal_pattern_set})")

        # let's see which segments could be in play for the provided pattern
        # long-hand for sanity
        available_segments = set()
        for this_signal in this_signal_pattern:
            for this_segment in range(1, 8):
                if this_signal in segment_possibilities[this_segment]:
                    available_segments.add(this_segment)
        print(
            f"Handling {this_signal_pattern} -> available segments are : {available_segments}"
        )
        # ok, we know which segments we are working with, and the length, which patterns are possible
        potential_matches = set()
        match_segments = set()
        for this_segment_pattern in valid_segments:
            if len(this_signal_pattern) == len(this_segment_pattern):
                print(f" - might match {this_segment_pattern}")
                # might be a match, but are all the segments we need in the pool ?
                this_segment_pattern_set = set([int(x) for x in this_segment_pattern])
                if this_segment_pattern_set.issubset(available_segments):
                    # woo-hoo - this looks good..
                    # for now adding this - but we're missing a trick here..
                    # this doesn't handle the case where we have known values in the list
                    # e.g. signal a is in the input, we know signal a is segment 1
                    #      segment 1 is not in the pattern but because signal b has all the options except 1
                    #      we can still match everything because the set of available segments is complete
                    #      this is a problem, we will potentially need to fix this in a minute..
                    #
                    #  This might be solved be examining each input signal and seeing if that signal's possible segments are in the pattern.
                    #  That still doesn't solve everything but it's a start.. that'll be the re-write when lazy fails
                    #
                    #  Update: it's 6 minutes later, lazy failed.. on to add this..
                    #
                    #  for each signal we have received, are any of those options in the segment list for this pattern ?
                    #   if not then this is bs..

                    for x in this_segment_pattern_set:
                        # are any of the segment possibilities in the signals ?
                        if segment_possibilities[x].isdisjoint(this_signal_pattern_set):
                            # no overlap - this is not a match..
                            print(
                                f" - BOO - DISQUALIFIED BECAUSE {segment_possibilities[x]} has no overlap with {this_signal_pattern_set}"
                            )

                    potential_matches.add(this_segment_pattern)
                    match_segments.update(this_segment_pattern_set)
        print(
            f"Handling {this_signal_pattern} -> potential matches are : {potential_matches}"
        )
        print(
            f"Handling {this_signal_pattern} -> potential segment matches are : {match_segments}"
        )

        # now we know what the potential matches are, we can start to whittle down the alternatives..
        # there are 2 different situations I think..
        # situation 1 - the perfect storm
        # - #signals (a,b) == #segments (7,8)  -> this means that signal a can only be 7 or 8,
        #                                         same for b, also that no other signals can be 7 or 8
        # situation 2 - the less perfect rainy day
        # - #signals (a, b) < #segments (1, 2, 3) -> this means that while we can't narrow down
        #                                            segments 1, 2, 3, we know that none of the other segments
        #                                            are valid for these signals ?? (not sure here)
        # let's begin..

        # perfect storm..
        the_signals = [x for x in this_signal_pattern]
        if len(match_segments) == len(the_signals):
            print(f"Perfect storm! {match_segments} and {the_signals}")
            # ok, so adjust the segment possibilities for the segments mentioned
            # the only options for them are now the intersection of the current options and the signals
            # part 1 - limit these segments to these signals only
            for this_segment in match_segments:
                segment_possibilities[this_segment].intersection_update(the_signals)
            # part 2 - remove these signals as possibilities from all the other segments
            for this_segment in [x for x in range(1, 8) if x not in match_segments]:
                segment_possibilities[this_segment].difference_update(the_signals)
            # and let's see what we have..
            print_segment_possibilities(segment_possibilities)
        else:
            print(f"IMPerfect storm :/ {match_segments} and {the_signals}")


input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
handle_one_line(input)
