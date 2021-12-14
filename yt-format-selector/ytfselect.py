#!/usr/bin/env python3

#
#  Selector for the preferred YT formats..
#  output should be either exit code 0 - output of the best format pair video+audio
#  or exit-code non-zero for not found..
#

import sys

preferred_audio = [140]
preferred_video = [399, 398, 397, 396, 244]


def is_int(s: str) -> bool:
    result = True
    try:
        i = int(s)
    except:
        result = False
    return result


def pick_best(preferences, available):
    """
    find the first preference in available or exit(2) if none found
    """
    for this_format in preferences:
        if this_format in available:
            return this_format
    exit(2)


def select_formats(filename: str):
    """
    Get the best format selection possible and print it
    """

    available_formats = dict()

    # Load the available formats..
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # ok, is this a format line that starts with a number ?
                parts = this_line.split(sep=None, maxsplit=1)
                if 2 == len(parts) and is_int(parts[0]):
                    format_code = int(parts[0])
                    format_desc = parts[1]
                    available_formats[format_code] = format_desc
    # got them.
    video = pick_best(preferred_video, available_formats)
    audio = pick_best(preferred_audio, available_formats)
    print(f"{video}+{audio}")


if __name__ == "__main__":
    if 2 != len(sys.argv):
        print(
            f'You need to pass one argument which is a file with the output from "youtube-dl -F $1'
        )
        exit(1)
    select_formats(sys.argv[1])
