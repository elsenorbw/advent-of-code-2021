#
#  Figure out how to figure out the riddle..
#


# new approach, recursion is your pattern-matchy little friend.

# We will be working with :
# Patterns - a combination of segments that represent a valid number
# Segments - numbered 1-7 inclusive, individual segments on the digital display digit
# Signals - a-g inclusive, the signals coming from the machine that need to be matched to segments


def get_valid_segment_patterns():
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
    return {
        0: set([int(x) for x in "123456"]),
        1: set([int(x) for x in "23"]),
        2: set([int(x) for x in "12457"]),
        3: set([int(x) for x in "12347"]),
        4: set([int(x) for x in "2367"]),
        5: set([int(x) for x in "13467"]),
        6: set([int(x) for x in "134567"]),
        7: set([int(x) for x in "123"]),
        8: set([int(x) for x in "1234567"]),
        9: set([int(x) for x in "123467"]),
    }


class SignalSegmentMap:
    def __init__(self) -> None:
        self.signals_for_segments = {
            1: {"a", "b", "c", "d", "e", "f", "g"},
            2: {"a", "b", "c", "d", "e", "f", "g"},
            3: {"a", "b", "c", "d", "e", "f", "g"},
            4: {"a", "b", "c", "d", "e", "f", "g"},
            5: {"a", "b", "c", "d", "e", "f", "g"},
            6: {"a", "b", "c", "d", "e", "f", "g"},
            7: {"a", "b", "c", "d", "e", "f", "g"},
        }
        self.segments_for_signals = {
            "a": {1, 2, 3, 4, 5, 6, 7},
            "b": {1, 2, 3, 4, 5, 6, 7},
            "c": {1, 2, 3, 4, 5, 6, 7},
            "d": {1, 2, 3, 4, 5, 6, 7},
            "e": {1, 2, 3, 4, 5, 6, 7},
            "f": {1, 2, 3, 4, 5, 6, 7},
            "g": {1, 2, 3, 4, 5, 6, 7},
        }

    def __repr__(self) -> str:
        result = f"SignalSegmentMap<"
        for this_segment in self.segments_for_signals:
            result += f" {this_segment}->{self.segments_for_signals[this_segment]}"
        result += ">"
        return result

    def get_segments_for_signal(self, signal: str):
        """
        Return the set of valid segments for a signal
        """
        return self.segments_for_signals[signal].copy()

    def update_for_matches(self, segments, signals):
        """
        Given a list of segments and potential matches we need to update the state.
        If the two are the same size then we can remove from both lists..
        we know that given (a,b)(1,2) that only a or b can be either 1 or 2
        given that we can remove 1 and 2 from all other signals and remove
        everything that is not a or b from 1 and 2.

        If they are not the same size then we have the situation where each signal
        can map to any of the segments however we cannot remove other signals from
        any segment because we don't know which segment is not actually correct.
        """

        # 1) Always limit the signals specified to be the intersection of what they currently could be
        #    and the segments provided. For example if we know that signal (a) can only be [1, 2, 3] already
        #    and the signals matched here are (1, 3, 5, 7) then we know that (a) must now be in (1, 3)
        for this_signal in signals:
            self.segments_for_signals[this_signal].intersection_update(segments)

        # 2) Now that we have that arranged we can potentially remove the
        #    options where the two sets are the same size..
        if len(segments) == len(signals):
            for this_signal in [
                s for s in self.segments_for_signals.keys() if s not in signals
            ]:
                self.segments_for_signals[this_signal].difference_update(segments)


def can_they_match(the_signal, the_pattern, signal_map):
    # recursion and other animals here..
    # right, we have a signal and a pattern that it may match..
    # so going to grab the first element out of the signal
    # and iterate through the possible values that it could have
    # until we find one that works or we run out of options.
    #
    remaining_signal = the_signal.copy()
    this_signal_part = remaining_signal.pop()

    # so, what are the available segments for this signal part ?
    available_segments = signal_map.get_segments_for_signal(this_signal_part)
    for this_segment in available_segments:
        # is this segment in the remaining pattern ?
        if this_segment in the_pattern:
            print(
                f"can_they_match({the_signal}, {the_pattern}) -> working on {this_signal_part} could be {this_segment}"
            )
            # we could be finished ?
            if len(remaining_signal) == 0:
                print(f"GOT ONE!")
                return True
            else:
                # ok, we're going to try this segment as an option for this signal..
                # generate a remaining set of pattern..
                remaining_pattern = the_pattern.copy()
                # and remove the one we're trying
                remaining_pattern.remove(this_segment)
                # time for recursion..
                result = can_they_match(remaining_signal, remaining_pattern, signal_map)
                if result:
                    return True
    print("-NOPE")
    return False


def match_one_pattern(the_signal, pattern_list, signal_map):
    """
    Run the logic for matching one pattern and reducing the signal
    map appropriately given what we already know..
    """

    # 1) Get a list of the patterns that match the input signals..
    matches = []
    for this_pattern in pattern_list.values():
        if len(this_pattern) == len(the_signal):
            print(f"- comparing {this_pattern} with {the_signal}")
            # ok, they are the same length, but is it possible ?
            potential_match = can_they_match(the_signal, this_pattern, signal_map)
            if potential_match:
                print(f"MATCH: {this_pattern} with {the_signal}")
                matches.append(this_pattern)

    # 2) Appropriately adjust the signal_map based on what we have learned
    print(f"Matches are : {matches}")
    # get a list of all the unique matching segment possibilities
    segment_possiblities = set()
    for this_match in matches:
        segment_possiblities.update(this_match)
    signal_map.update_for_matches(segment_possiblities, the_signal)


def match_signals_to_segments(signal_list):
    """
    Given a list of all the signals in the input, return a mapping of signals to segments
    """

    # We need to store a list of the possible mappings for signals <-> segments
    sig_map = SignalSegmentMap()
    print(sig_map)

    # and we need the segment patterns
    patterns = get_valid_segment_patterns()

    # ok, we can start to loop at this point..
    for this_signal in signal_list:
        # turn the signal into a set
        this_signal_set = set([x for x in this_signal])
        #  try to solve this pattern..
        match_one_pattern(this_signal_set, patterns, sig_map)
        #  and see what we're looking like now..
        print(sig_map)


# order the characters in the provided string
def sort_string(s: str) -> str:
    return "".join(sorted(s))


def handle_one_line(the_line: str):
    # let's get everything nicely into tokens..
    parts = the_line.split("|")
    left_tokens = [x for x in parts[0].split(" ") if x != ""]
    right_tokens = [x for x in parts[1].split(" ") if x != ""]
    all_tokens = left_tokens + right_tokens
    print(f"All the tokens : {all_tokens}")
    # let's order the characters in each one to make life easier..
    ordered_tokens = sorted([sort_string(x) for x in all_tokens], key=len)
    print(f"        Sorted : {ordered_tokens}")

    # ok, that's the messing around done, time to match signals to segments
    match_signals_to_segments(ordered_tokens)


if __name__ == "__main__":
    input = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    handle_one_line(input)
