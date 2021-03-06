# --- Day 9: Smoke Basin ---

# These caves seem to be lava tubes. Parts are even still volcanically active;
# small hydrothermal vents release smoke into the caves that slowly settles
# like rain.

# If you can model how the smoke flows through the caves, you might be able to
# avoid it and be that much safer. The submarine generates a heightmap of the
# floor of the nearby caves for you (your puzzle input).

# Smoke flows to the lowest point of the area it's in. For example, consider
# the following heightmap:

# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678

# Each number corresponds to the height of a particular location, where 9 is
# the highest and 0 is the lowest a location can be.

# Your first goal is to find the low points - the locations that are lower than
# any of its adjacent locations. Most locations have four adjacent locations
# (up, down, left, and right); locations on the edge or corner of the map have
# three or two adjacent locations, respectively. (Diagonal locations do not
# count as adjacent.)

# In the above example, there are four low points, all highlighted: two are in
# the first row (a 1 and a 0), one is in the third row (a 5), and one is in the
# bottom row (also a 5). All other locations on the heightmap have some lower
# adjacent location, and so are not low points.

# The risk level of a low point is 1 plus its height. In the above example,
# the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk
# levels of all low points in the heightmap is therefore 15.

# Find all of the low points on your heightmap. What is the sum of the risk
# levels of all low points on your heightmap?
import math


def leftof(location):
    x, y = location
    return (x - 1, y)


def rightof(location):
    x, y = location
    return (x + 1, y)


def upof(location):
    x, y = location
    return (x, y - 1)


def downof(location):
    x, y = location
    return (x, y + 1)


class CavernFloor:
    def __init__(self, filename: str = None) -> None:
        self._reset()
        if filename is not None:
            self.load_floor_from_file(filename)

    def _reset(self):
        self.spots = dict()
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def _ensure_bounds(self, x, y):
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

    def _set_location_depth(self, x: int, y: int, depth: int):
        """
        Store one floor depth correctly
        """
        self.spots[(x, y)] = depth
        self._ensure_bounds(x, y)

    def _get_depth_str(self, x, y):
        """
        Return the depth string or '.' if missing
        """
        key = (x, y)
        if key in self.spots:
            result = str(self.spots[key])
        else:
            result = "."
        return result

    def load_floor_from_file(self, filename: str):
        """
        Load a fresh floor from the file specified
        """
        self.spots = dict()
        with open(filename, "r") as f:
            this_y = 0
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    for this_x, this_depth_str in enumerate(this_line):
                        self._set_location_depth(this_x, this_y, int(this_depth_str))
                    this_y += 1

    def _is_low_point(self, location) -> bool:
        """
        True if this location has no orthagonal neighbours with lower values
        """
        x, y = location
        this_val = self._get_value_at_location(location)
        # grab each neighbour and see if they are lower..
        target_locations = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for this_target in target_locations:
            target_val = self._get_value_at_location(this_target, this_val + 1)
            if target_val <= this_val:
                # done..
                return False
        return True

    def _get_value_at_location(self, location, default=None) -> int:
        if location in self.spots:
            result = self.spots[location]
        else:
            result = default
        return result

    def calculate_low_risk(self):
        """
        Basically the part 1 solve.
        For each spot on the map, if it is lower than its orthagonal existing neighbours,
        then increment the total by 1+the depth of that spot
        """
        total = 0
        for this_location in self.spots:
            if self._is_low_point(this_location):
                total += 1 + self._get_value_at_location(this_location)
        return total

    def find_low_points(self):
        """
        Return a list of low-point locations
        """
        result = []
        for this_location in self.spots:
            if self._is_low_point(this_location):
                result.append(this_location)
        return result

    def _find_places_from_here(self, location, already_seen):
        """
        how many orthoganol-connections is this shape ?
        """
        # been here before ? die then..
        if location in already_seen:
            return 0
        # never seen this place.. cool... is it a valid place ?
        if location not in self.spots:
            return 0
        # it is a valid place - sold..
        already_seen.add(location)
        total = 1
        total += self._find_places_from_here(leftof(location), already_seen)
        total += self._find_places_from_here(rightof(location), already_seen)
        total += self._find_places_from_here(upof(location), already_seen)
        total += self._find_places_from_here(downof(location), already_seen)
        return total

    def find_basin_size(self, location):
        """
        Find the count of all the points connected to this location
        """
        # a little worried about having looping basins.. so going to keep a list and make sure we don't double back..
        places_we_have_seen = set()
        total = self._find_places_from_here(location, places_we_have_seen)
        return total

    def remove_high_ground(self):
        """
        Get rid of anything that's a 9
        """
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                if 9 == self.spots[(x, y)]:
                    del self.spots[(x, y)]

    def __repr__(self) -> str:
        result = f"CavernFloor [{self.max_x - self.min_x + 1}x{self.max_y - self.min_y + 1}] ({self.min_x},{self.min_y})-({self.max_x},{self.max_y})\n"
        for y in range(self.min_y, self.max_y + 1):
            s = ""
            for x in range(self.min_x, self.max_x + 1):
                s += self._get_depth_str(x, y)
            result += f"{s}\n"
        return result


def part1(filename: str) -> int:
    """
    Solve part1
    """
    result = 0
    cave = CavernFloor(filename)
    print(cave)
    result = cave.calculate_low_risk()

    return result


def part2(filename: str) -> int:
    """
    Solve part2
    """
    cave = CavernFloor(filename)
    low_points = cave.find_low_points()
    cave.remove_high_ground()
    print(cave)
    print(low_points)
    basin_sizes = [cave.find_basin_size(location) for location in low_points]
    print(basin_sizes)
    sorted_sizes = sorted(basin_sizes, reverse=True)
    print(sorted_sizes)
    top_3 = sorted_sizes[:3]
    print(top_3)
    result = math.prod(top_3)
    return result


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    expected_test_part1 = 15
    expected_test_part2 = 1134

    test1 = part1(test_filename)
    print(f"Test part 1 output: {test1} (should be {expected_test_part1})")
    assert test1 == expected_test_part1

    puzz1 = part1(puzzle_filename)
    print(f"Part 1 output: {puzz1}")

    test2 = part2(test_filename)
    print(f"Test part 2 output: {test2} (should be {expected_test_part2})")
    assert test2 == expected_test_part2

    puzz2 = part2(puzzle_filename)
    print(f"Part 2 output: {puzz2}")
