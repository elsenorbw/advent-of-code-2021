# --- Day 19: Beacon Scanner ---

# As your probe drifted down through this area, it released an assortment of beacons and scanners into the water.
# It's difficult to navigate in the pitch black open waters of the ocean trench, but if you can build a map of the
# trench using data from the scanners, you should be able to safely reach the bottom.

# The beacons and scanners float motionless in the water; they're designed to maintain the same position for long
# periods of time. Each scanner is capable of detecting all beacons in a large cube centered on the scanner; beacons
# that are at most 1000 units away from the scanner in each of the three axes (x, y, and z) have their precise position
# determined relative to the scanner. However, scanners cannot detect other scanners. The submarine has automatically
# summarized the relative positions of beacons detected by each scanner (your puzzle input).

# For example, if a scanner is at x,y,z coordinates 500,0,-500 and there are beacons at -500,1000,-1500 and 1501,0,-500,
# the scanner could report that the first beacon is at -1000,1000,-1000 (relative to the scanner) but would not detect
# the second beacon at all.

# Unfortunately, while each scanner can report the positions of all detected beacons relative to itself, the scanners
# do not know their own position. You'll need to determine the positions of the beacons and scanners yourself.

# The scanners and beacons map a single contiguous 3d region. This region can be reconstructed by finding pairs of
# scanners that have overlapping detection regions such that there are at least 12 beacons that both scanners detect
# within the overlap. By establishing 12 common beacons, you can precisely determine where the scanners are relative
# to each other, allowing you to reconstruct the beacon map one scanner at a time.

# For a moment, consider only two dimensions. Suppose you have the following scanner reports:

# --- scanner 0 ---
# 0,2
# 4,1
# 3,3

# --- scanner 1 ---
# -1,-1
# -5,0
# -2,1

# Drawing x increasing rightward, y increasing upward, scanners as S, and beacons as B, scanner 0 detects this:

# ...B.
# B....
# ....B
# S....

# Scanner 1 detects this:

# ...B..
# B....S
# ....B.

# For this example, assume scanners only need 3 overlapping beacons. Then, the beacons visible to both scanners overlap
# to produce the following complete map:

# ...B..
# B....S
# ....B.
# S.....

# Unfortunately, there's a second problem: the scanners also don't know their rotation or facing direction. Due to magnetic
# alignment, each scanner is rotated some integer number of 90-degree turns around all of the x, y, and z axes. That is, one
# scanner might call a direction positive x, while another scanner might call that direction negative y. Or, two scanners might
# agree on which direction is positive x, but one scanner might be upside-down from the perspective of the other scanner.
# In total, each scanner could be in any of 24 different orientations: facing positive or negative x, y, or z, and considering
# any of four directions "up" from that facing.

# For example, here is an arrangement of beacons as seen from a scanner in the same position but in different orientations:

# --- scanner 0 ---
# -1,-1,1
# -2,-2,2
# -3,-3,3
# -2,-3,1
# 5,6,-4
# 8,0,7

# --- scanner 0 ---
# 1,-1,1
# 2,-2,2
# 3,-3,3
# 2,-1,3
# -5,4,-6
# -8,-7,0

# --- scanner 0 ---
# -1,-1,-1
# -2,-2,-2
# -3,-3,-3
# -1,-3,-2
# 4,6,5
# -7,0,8

# --- scanner 0 ---
# 1,1,-1
# 2,2,-2
# 3,3,-3
# 1,3,-2
# -4,-6,5
# 7,0,8

# --- scanner 0 ---
# 1,1,1
# 2,2,2
# 3,3,3
# 3,1,2
# -6,-4,-5
# 0,7,-8

# By finding pairs of scanners that both see at least 12 of the same beacons, you can assemble the entire map. For example, consider the following report:

# --- scanner 0 ---
# 404,-588,-901
# 528,-643,409
# -838,591,734
# 390,-675,-793
# -537,-823,-458
# -485,-357,347
# -345,-311,381
# -661,-816,-575
# -876,649,763
# -618,-824,-621
# 553,345,-567
# 474,580,667
# -447,-329,318
# -584,868,-557
# 544,-627,-890
# 564,392,-477
# 455,729,728
# -892,524,684
# -689,845,-530
# 423,-701,434
# 7,-33,-71
# 630,319,-379
# 443,580,662
# -789,900,-551
# 459,-707,401

# --- scanner 1 ---
# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# 95,138,22
# -476,619,847
# -340,-569,-846
# 567,-361,727
# -460,603,-452
# 669,-402,600
# 729,430,532
# -500,-761,534
# -322,571,750
# -466,-666,-811
# -429,-592,574
# -355,545,-477
# 703,-491,-529
# -328,-685,520
# 413,935,-424
# -391,539,-444
# 586,-435,557
# -364,-763,-893
# 807,-499,-711
# 755,-354,-619
# 553,889,-390

# --- scanner 2 ---
# 649,640,665
# 682,-795,504
# -784,533,-524
# -644,584,-595
# -588,-843,648
# -30,6,44
# -674,560,763
# 500,723,-460
# 609,671,-379
# -555,-800,653
# -675,-892,-343
# 697,-426,-610
# 578,704,681
# 493,664,-388
# -671,-858,530
# -667,343,800
# 571,-461,-707
# -138,-166,112
# -889,563,-600
# 646,-828,498
# 640,759,510
# -630,509,768
# -681,-892,-333
# 673,-379,-804
# -742,-814,-386
# 577,-820,562

# --- scanner 3 ---
# -589,542,597
# 605,-692,669
# -500,565,-823
# -660,373,557
# -458,-679,-417
# -488,449,543
# -626,468,-788
# 338,-750,-386
# 528,-832,-391
# 562,-778,733
# -938,-730,414
# 543,643,-506
# -524,371,-870
# 407,773,750
# -104,29,83
# 378,-903,-323
# -778,-728,485
# 426,699,580
# -438,-605,-362
# -469,-447,-387
# 509,732,623
# 647,635,-688
# -868,-804,481
# 614,-800,639
# 595,780,-596

# --- scanner 4 ---
# 727,592,562
# -293,-554,779
# 441,611,-461
# -714,465,-776
# -743,427,-804
# -660,-479,-426
# 832,-632,460
# 927,-485,-438
# 408,393,-506
# 466,436,-512
# 110,16,151
# -258,-428,682
# -393,719,612
# -211,-452,876
# 808,-476,-593
# -575,615,604
# -485,667,467
# -680,325,-822
# -627,-443,-432
# 872,-547,-609
# 833,512,582
# 807,604,487
# 839,-516,451
# 891,-625,532
# -652,-548,-490
# 30,-46,-14

# Because all coordinates are relative, in this example, all "absolute" positions will be expressed relative to scanner 0 (using the orientation of scanner 0 and as if scanner 0 is at coordinates 0,0,0).

# Scanners 0 and 1 have overlapping detection cubes; the 12 beacons they both detect (relative to scanner 0) are at the following coordinates:

# -618,-824,-621
# -537,-823,-458
# -447,-329,318
# 404,-588,-901
# 544,-627,-890
# 528,-643,409
# -661,-816,-575
# 390,-675,-793
# 423,-701,434
# -345,-311,381
# 459,-707,401
# -485,-357,347

# These same 12 beacons (in the same order) but from the perspective of scanner 1 are:

# 686,422,578
# 605,423,415
# 515,917,-361
# -336,658,858
# -476,619,847
# -460,603,-452
# 729,430,532
# -322,571,750
# -355,545,-477
# 413,935,-424
# -391,539,-444
# 553,889,-390

# Because of this, scanner 1 must be at 68,-1246,-43 (relative to scanner 0).

# Scanner 4 overlaps with scanner 1; the 12 beacons they both detect (relative to scanner 0) are:

# 459,-707,401
# -739,-1745,668
# -485,-357,347
# 432,-2009,850
# 528,-643,409
# 423,-701,434
# -345,-311,381
# 408,-1815,803
# 534,-1912,768
# -687,-1600,576
# -447,-329,318
# -635,-1737,486

# So, scanner 4 is at -20,-1133,1061 (relative to scanner 0).

# Following this process, scanner 2 must be at 1105,-1205,1229 (relative to scanner 0) and scanner 3 must be at -92,-2380,-20 (relative to scanner 0).

# The full list of beacons (relative to scanner 0) is:

# -892,524,684
# -876,649,763
# -838,591,734
# -789,900,-551
# -739,-1745,668
# -706,-3180,-659
# -697,-3072,-689
# -689,845,-530
# -687,-1600,576
# -661,-816,-575
# -654,-3158,-753
# -635,-1737,486
# -631,-672,1502
# -624,-1620,1868
# -620,-3212,371
# -618,-824,-621
# -612,-1695,1788
# -601,-1648,-643
# -584,868,-557
# -537,-823,-458
# -532,-1715,1894
# -518,-1681,-600
# -499,-1607,-770
# -485,-357,347
# -470,-3283,303
# -456,-621,1527
# -447,-329,318
# -430,-3130,366
# -413,-627,1469
# -345,-311,381
# -36,-1284,1171
# -27,-1108,-65
# 7,-33,-71
# 12,-2351,-103
# 26,-1119,1091
# 346,-2985,342
# 366,-3059,397
# 377,-2827,367
# 390,-675,-793
# 396,-1931,-563
# 404,-588,-901
# 408,-1815,803
# 423,-701,434
# 432,-2009,850
# 443,580,662
# 455,729,728
# 456,-540,1869
# 459,-707,401
# 465,-695,1988
# 474,580,667
# 496,-1584,1900
# 497,-1838,-617
# 527,-524,1933
# 528,-643,409
# 534,-1912,768
# 544,-627,-890
# 553,345,-567
# 564,392,-477
# 568,-2007,-577
# 605,-1665,1952
# 612,-1593,1893
# 630,319,-379
# 686,-3108,-505
# 776,-3184,-501
# 846,-3110,-434
# 1135,-1161,1235
# 1243,-1093,1063
# 1660,-552,429
# 1693,-557,386
# 1735,-437,1738
# 1749,-1800,1813
# 1772,-405,1572
# 1776,-675,371
# 1779,-442,1789
# 1780,-1548,337
# 1786,-1538,337
# 1847,-1591,415
# 1889,-1729,1762
# 1994,-1805,1792

# In total, there are 79 beacons.

# Assemble the full map of beacons. How many beacons are there?

# To begin, get your puzzle input.


#
#  THINKING: Ok, this looks hard, not really sure how to approach it.
#            It must be about relative positions for the points found in each scanner as any one point could be any other one point anywhere
#            so it must be that you find X points that all are correlated with each other in each axis..
#            Given the way the scanners work, the points near each other are probably (but not definitely) a match for each other
#            since it's a cube from where the scanner is, and the overlaps of the cubes should be relatively simple..
#            actually, is it necessarily true that all 12 must be in a line on one axis ?
#            Thinking more.. no, because a big swing in Y or Z would have additional spots on the X axis (say) in one of the two sectors..
#            Is there some way we can turn the differences between each point into an easy to search numerical value ?
#            abs(xdiff), abs(ydiff), abs(zdiff) perhaps, but we don't know which axis is which so... can we just sort them into largest values ?
#            That would give us a problem of coincidence whereby two different pairs have different X axes but both show as matching in X.. hmm.
#
#            So the very long way would be to take a given point in a given list and try the matching as if it were correlated with each point in a different scanner.
#             - translate everything as if they were the same point and then see if we get 12 matches or not. This seems like it's going to take a very long time.
#            There's probably some mileage in finding a matching pair and working from there as a possibility.
#


def manhattan(a, b):
    small = min(a, b)
    big = max(a, b)
    return big - small


class Scanner:
    def __init__(self, scanner_number: int) -> None:
        self.points = list()
        self.x = None
        self.y = None
        self.z = None
        self.scanner_number = scanner_number
        self.config_idx = 0
        self.configurations = list()

        for x in range(3):
            for y in range(3):
                for z in range(3):
                    if x != y and x != z and y != z:
                        # got a good xyz set..
                        for x_flip in (False, True):
                            for y_flip in (False, True):
                                for z_flip in (False, True):
                                    # these aren't exclusive
                                    self.configurations.append(
                                        (x, y, z, x_flip, y_flip, z_flip)
                                    )

    def __str__(self) -> str:
        result = f"Scanner {self.scanner_number} ({len(self.points)} points, "
        if self.x is not None:
            result += f"at=({self.x},{self.y},{self.z})"
        else:
            result += "floating"
        result += ")"
        return result

    def set_configuration(self, configuration_index: int):
        self.config_idx = configuration_index

    def situated(self):
        return self.x is not None

    def add_point(self, x: int, y: int, z: int):
        self.points.append((x, y, z))

    def get_points(self, configuration=None):
        """
        Return a list with all the points in it for a given configuration
        """
        if configuration is None:
            configuration = self.config_idx

        result = list()
        for this_point in self.points:
            x = this_point[self.configurations[configuration][0]]
            y = this_point[self.configurations[configuration][1]]
            z = this_point[self.configurations[configuration][2]]
            if self.configurations[configuration][3]:
                x = -x
            if self.configurations[configuration][4]:
                y = -y
            if self.configurations[configuration][5]:
                z = -z

            # and apply our starting offsets..
            if self.x is not None:
                x += self.x
                y += self.y
                z += self.z

            result.append((x, y, z))
        return result

    def get_configuration_index_range(self):
        return range(len(self.configurations))

    def set_location(self, x: int, y: int, z: int):
        """
        set the location and orientation in space
        """
        self.x = x
        self.y = y
        self.z = z

    def calculate_manhattan_to(self, other):
        """
        How manhattan far away from other are we ?
        it's basically larger-smaller in each of the dimensions
        """
        x = manhattan(self.x, other.x)
        y = manhattan(self.y, other.y)
        z = manhattan(self.z, other.z)
        result = x + y + z
        return result

    def align_other(self, other):
        """
        Try and see whether there is an alignment and offset that hits at least 12 matches
        Assuming that the rotation and ordering and location of this scanner is correct
        """
        our_points = self.get_points()
        our_points_set = set(our_points)
        for config_index in other.get_configuration_index_range():
            # get the base list for this configuration
            other_points = other.get_points(config_index)
            # ok, so we need to try and match each of these points with all of our points..
            for our_point in our_points:
                for other_point in other_points:
                    # so, to make this work we will need to calculate the offset that we would have to apply to make these two the same
                    # our_points are absolute universe coordinates, so 100, 100, 100 is just that, the points have been translated.
                    # given we know the configuration has been applied to other, we just need to do the maths:
                    # an absolute correct coordinate of say 1000, with a -200 value in other means we need a 1200 starting point for other
                    # therefore other.x_position := our.x - other_point.x
                    x_position = our_point[0] - other_point[0]
                    y_position = our_point[1] - other_point[1]
                    z_position = our_point[2] - other_point[2]
                    #
                    #  ok, cool.. let's create an adjusted points list for the other scanner
                    #
                    adjusted_other_points = [
                        (x + x_position, y + y_position, z + z_position)
                        for x, y, z in other_points
                    ]
                    adjusted_other_points_set = set(adjusted_other_points)
                    # how many match now ?
                    matching = our_points_set.intersection(adjusted_other_points_set)
                    if len(matching) >= 12:
                        print(f"Solved a match!")
                        other.set_configuration(config_index)
                        other.set_location(x_position, y_position, z_position)
                        return True

        # well that was a bust..
        return False


class ScannerField:
    def __init__(self):
        self.scanners = dict()

    def load_file(self, filename: str):
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # is this the start of a new scanner ?
                    if this_line.startswith("--- scanner "):
                        # get the scanner number
                        parts = this_line.split(" ")
                        scanner_no = int(parts[2])
                        # create and store a new scanner..
                        the_scanner = Scanner(scanner_no)
                        self.scanners[scanner_no] = the_scanner
                    else:
                        # regular x,y,z line..
                        vals = this_line.split(",")
                        coords = (int(vals[0]), int(vals[1]), int(vals[2]))
                        self.scanners[scanner_no].add_point(*coords)

    def print(self):
        """
        Output the current scanner list
        """
        print(f"ScannerField ({len(self.scanners)} scanners)")
        for this_scanner in self.scanners:
            print(f" - {self.scanners[this_scanner]}")

    def situated(self):
        return all([s.situated() for s in self.scanners.values()])

    def get_unsituated(self):
        return [s for s in self.scanners.values() if not s.situated()]

    def get_situated(self):
        return [s for s in self.scanners.values() if s.situated()]

    def count_points(self):
        all_points = set()
        for this_scanner in self.scanners.values():
            these_points = set(this_scanner.get_points())
            all_points.update(these_points)
        return len(all_points)

    def largest_manhattan_distance(self):
        """
        What is the largest manhattan distance between any two scanners..
        """
        best_manhattan = 0
        for a in self.scanners.values():
            for b in self.scanners.values():
                this_manhattan = a.calculate_manhattan_to(b)
                if this_manhattan > best_manhattan:
                    print(f"New best Manhattan is {this_manhattan} between {a} and {b}")
                    best_manhattan = this_manhattan
        return best_manhattan

    def align_scanners(self):
        """
        Figure out which scanners live where
        """
        # Setup an initial scanner..
        self.scanners[0].set_location(0, 0, 0)

        # Keep on correlating until we're done
        compared = set()
        while not self.situated():
            # loop through all the unsituated scanners and try to situate them..
            unsituated = self.get_unsituated()
            situated = self.get_situated()
            print(
                f"Top of the loop, need to situate {len(unsituated)} against {len(situated)}"
            )
            for this_target in unsituated:
                for this_base in situated:
                    key = (this_target.scanner_number, this_base.scanner_number)
                    if key not in compared:
                        compared.add(key)
                        print(f"Trying to align {this_target} against {this_base}")
                        if this_base.align_other(this_target):
                            break


def part1(filename: str):
    field = ScannerField()
    field.load_file(filename)
    field.print()
    field.align_scanners()
    result = field.count_points()
    return result


def part2(filename: str):
    field = ScannerField()
    field.load_file(filename)
    field.print()
    field.align_scanners()
    result = field.largest_manhattan_distance()
    return result


def silly():
    s = Scanner(999)
    s.add_point(1, 2, 3)
    for idx in range(48):
        l = s.get_points(idx)
        print(l)
    exit(1)


if __name__ == "__main__":
    # silly()
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"

    if False:
        test1 = part1(test_filename)
        test1_expected = 79
        print(f"test1 got {test1}, should be {test1_expected}")
        assert test1 == test1_expected
        puzz1 = part1(puzzle_filename)
        print(f"Puzzle part 1 is {puzz1}")

    test2 = part2(test_filename)
    test2_expected = 3621
    print(f"test2 got {test2}, should be {test2_expected}")
    assert test2 == test2_expected
    puzz2 = part2(puzzle_filename)
    print(f"Part2 is {puzz2}")
