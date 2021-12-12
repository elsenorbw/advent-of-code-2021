# --- Day 12: Passage Pathing ---

# With your submarine's subterranean subsystems subsisting suboptimally,
# the only way you're getting out of this cave anytime soon is by finding a
# path yourself. Not just a path - the only way to know if you've found the
# best path is to find all of them.

# Fortunately, the sensors are still mostly working, and so you build a rough
# map of the remaining caves (your puzzle input). For example:

# start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end

# This is a list of how all of the caves are connected. You start in the cave
# named start, and your destination is the cave named end. An entry like b-d
# means that cave b is connected to cave d - that is, you can move between
# them.

# So, the above cave system looks roughly like this:

#     start
#     /   \
# c--A-----b--d
#     \   /
#      end

# Your goal is to find the number of distinct paths that start at start, end at
# end, and don't visit small caves more than once. There are two types of
# caves: big caves (written in uppercase, like A) and small caves (written in
# lowercase, like b). It would be a waste of time to visit any small cave more
# than once, but big caves are large enough that it might be worth visiting
# them multiple times. So, all paths you find should visit small caves at most
# once, and can visit big caves any number of times.

# Given these rules, there are 10 paths through this example cave system:

# start,A,b,A,c,A,end
# start,A,b,A,end
# start,A,b,end
# start,A,c,A,b,A,end
# start,A,c,A,b,end
# start,A,c,A,end
# start,A,end
# start,b,A,c,A,end
# start,b,A,end
# start,b,end

# (Each line in the above list corresponds to a single path; the caves visited
# by that path are listed in the order they are visited and separated by
# commas.)

# Note that in this cave system, cave d is never visited by any path: to do so,
# cave b would need to be visited twice (once on the way to cave d and a second
# time when returning from cave d), and since cave b is small, this is not
# allowed.

# Here is a slightly larger example:

# dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc

# The 19 paths through it are as follows:

# start,HN,dc,HN,end
# start,HN,dc,HN,kj,HN,end
# start,HN,dc,end
# start,HN,dc,kj,HN,end
# start,HN,end
# start,HN,kj,HN,dc,HN,end
# start,HN,kj,HN,dc,end
# start,HN,kj,HN,end
# start,HN,kj,dc,HN,end
# start,HN,kj,dc,end
# start,dc,HN,end
# start,dc,HN,kj,HN,end
# start,dc,end
# start,dc,kj,HN,end
# start,kj,HN,dc,HN,end
# start,kj,HN,dc,end
# start,kj,HN,end
# start,kj,dc,HN,end
# start,kj,dc,end

# Finally, this even larger example has 226 paths through it:

# fs-end
# he-DX
# fs-he
# start-DX
# pj-DX
# end-zg
# zg-sl
# zg-pj
# pj-he
# RW-he
# fs-DX
# pj-RW
# zg-RW
# start-pj
# he-WI
# zg-he
# pj-fs
# start-RW

# How many paths through this cave system are there that visit small caves at
# most once?


from os import path


class Mapper:
    def __init__(self) -> None:
        self.connections = dict()

    def __repr__(self) -> str:
        result = f"Mapper<{len(self.connections)} nodes>"
        return result

    def is_large_cave(cave: str) -> bool:
        """
        return true if the name passed is all uppercase
        """
        ucase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        char_is_upper = [x in ucase for x in cave]
        all_upper = all(char_is_upper)
        return all_upper

    def add_cave_mapping(self, cave_one, cave_two):
        """
        store the mapping between these two caves
        """
        if cave_one not in self.connections:
            self.connections[cave_one] = set()
        if cave_two not in self.connections:
            self.connections[cave_two] = set()
        # and now add the links
        self.connections[cave_one].add(cave_two)
        self.connections[cave_two].add(cave_one)

    def load_file(self, filename: str):
        """
        Load a file of the cave links
        """
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # actual link line..
                    caves = this_line.split("-")
                    # there should be 2
                    assert len(caves) == 2
                    self.add_cave_mapping(caves[0], caves[1])

    def find_routes_from_here(self, this_node, path_so_far, all_paths):
        """
        Starting from here, list out all the routes to the "end" node
        """
        # 1) Add this node to the path so far, need to know we were here
        path_so_far.append(this_node)

        # 2) Check each of the places we can go..
        for next_node in self.connections[this_node]:
            # a) This could be the last node - score..
            if "end" == next_node:
                all_paths.add(tuple(path_so_far + ["end"]))
            else:
                # ok, it's a mid-path node.. can we go here ?
                if Mapper.is_large_cave(next_node) or next_node not in path_so_far:
                    self.find_routes_from_here(next_node, path_so_far, all_paths)

        # 3) Remove this node from the path so far, we are done..
        path_so_far.pop()

    def enumerate_paths(self):
        """
        List out all the possible paths from start to finish
        """
        all_paths = set()
        path_so_far = []

        # starting at "start"
        self.find_routes_from_here("start", path_so_far, all_paths)

        return all_paths


def part1(filename: str) -> int:
    """
    Run the part1 logic
    """
    m = Mapper()
    m.load_file(filename)
    print(m)
    all_paths = m.enumerate_paths()
    print(f"Paths ({len(all_paths)}) : {all_paths}")
    return len(all_paths)


if __name__ == "__main__":
    part1_tests = [("test_10.txt", 10), ("test_19.txt", 19), ("test_226.txt", 226)]
    puzzle_filename = "puzzle_input.txt"

    # Run part1 tests
    for filename, expected in part1_tests:
        actual = part1(filename)
        print(f"Testing with {filename}, got {actual}, expected {expected}")
        assert actual == expected

    # run the actual part1
    puzz1 = part1(puzzle_filename)
    print(f"Actual Part1 answer is {puzz1}")
