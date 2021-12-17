# --- Day 15: Chiton ---

# You've almost reached the exit of the cave, but the walls are getting closer
# together. Your submarine can barely still fit, though; the main problem is
# that the walls of the cave are covered in chitons, and it would be best not
# to bump any of them.

# The cavern is large, but has a very low ceiling, restricting your motion to
# two dimensions. The shape of the cavern resembles a square; a quick scan of
# chiton density produces a map of risk level throughout the cave (your puzzle
# input). For example:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581

# You start in the top left position, your destination is the bottom right
# position, and you cannot move diagonally. The number at each position is its
# risk level; to determine the total risk of an entire path, add up the risk
# levels of each position you enter (that is, don't count the risk level of
# your starting position unless you enter it; leaving it adds no risk to your
# total).

# Your goal is to find a path with the lowest total risk. In this example, a
# path with the lowest total risk is highlighted here:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581

# The total risk of this path is 40 (the starting position is never entered,
# so its risk is not counted).

# What is the lowest total risk of any path from the top left to the bottom
# right?

# --- Part Two ---

# Now that you know how to find low-risk paths in the cave, you can try to find your way out.

# The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

# 8 9 1 2 3
# 9 1 2 3 4
# 1 2 3 4 5
# 2 3 4 5 6
# 3 4 5 6 7

# Each single digit above corresponds to the example position with a value of 8 on the top-left tile. Because the full map is actually five times larger in both dimensions, that position appears a total of 25 times, once in each duplicated tile, with the values shown above.

# Here is the full five-times-as-large version of the first example above, with the original map in the top left corner highlighted:

# 11637517422274862853338597396444961841755517295286
# 13813736722492484783351359589446246169155735727126
# 21365113283247622439435873354154698446526571955763
# 36949315694715142671582625378269373648937148475914
# 74634171118574528222968563933317967414442817852555
# 13191281372421239248353234135946434524615754563572
# 13599124212461123532357223464346833457545794456865
# 31254216394236532741534764385264587549637569865174
# 12931385212314249632342535174345364628545647573965
# 23119445813422155692453326671356443778246755488935
# 22748628533385973964449618417555172952866628316397
# 24924847833513595894462461691557357271266846838237
# 32476224394358733541546984465265719557637682166874
# 47151426715826253782693736489371484759148259586125
# 85745282229685639333179674144428178525553928963666
# 24212392483532341359464345246157545635726865674683
# 24611235323572234643468334575457944568656815567976
# 42365327415347643852645875496375698651748671976285
# 23142496323425351743453646285456475739656758684176
# 34221556924533266713564437782467554889357866599146
# 33859739644496184175551729528666283163977739427418
# 35135958944624616915573572712668468382377957949348
# 43587335415469844652657195576376821668748793277985
# 58262537826937364893714847591482595861259361697236
# 96856393331796741444281785255539289636664139174777
# 35323413594643452461575456357268656746837976785794
# 35722346434683345754579445686568155679767926678187
# 53476438526458754963756986517486719762859782187396
# 34253517434536462854564757396567586841767869795287
# 45332667135644377824675548893578665991468977611257
# 44961841755517295286662831639777394274188841538529
# 46246169155735727126684683823779579493488168151459
# 54698446526571955763768216687487932779859814388196
# 69373648937148475914825958612593616972361472718347
# 17967414442817852555392896366641391747775241285888
# 46434524615754563572686567468379767857948187896815
# 46833457545794456865681556797679266781878137789298
# 64587549637569865174867197628597821873961893298417
# 45364628545647573965675868417678697952878971816398
# 56443778246755488935786659914689776112579188722368
# 55172952866628316397773942741888415385299952649631
# 57357271266846838237795794934881681514599279262561
# 65719557637682166874879327798598143881961925499217
# 71484759148259586125936169723614727183472583829458
# 28178525553928963666413917477752412858886352396999
# 57545635726865674683797678579481878968159298917926
# 57944568656815567976792667818781377892989248891319
# 75698651748671976285978218739618932984172914319528
# 56475739656758684176786979528789718163989182927419
# 67554889357866599146897761125791887223681299833479

# Equipped with the full map, you can now find a path from the top left corner to the bottom right corner with the lowest total risk:

# 11637517422274862853338597396444961841755517295286
# 13813736722492484783351359589446246169155735727126
# 21365113283247622439435873354154698446526571955763
# 36949315694715142671582625378269373648937148475914
# 74634171118574528222968563933317967414442817852555
# 13191281372421239248353234135946434524615754563572
# 13599124212461123532357223464346833457545794456865
# 31254216394236532741534764385264587549637569865174
# 12931385212314249632342535174345364628545647573965
# 23119445813422155692453326671356443778246755488935
# 22748628533385973964449618417555172952866628316397
# 24924847833513595894462461691557357271266846838237
# 32476224394358733541546984465265719557637682166874
# 47151426715826253782693736489371484759148259586125
# 85745282229685639333179674144428178525553928963666
# 24212392483532341359464345246157545635726865674683
# 24611235323572234643468334575457944568656815567976
# 42365327415347643852645875496375698651748671976285
# 23142496323425351743453646285456475739656758684176
# 34221556924533266713564437782467554889357866599146
# 33859739644496184175551729528666283163977739427418
# 35135958944624616915573572712668468382377957949348
# 43587335415469844652657195576376821668748793277985
# 58262537826937364893714847591482595861259361697236
# 96856393331796741444281785255539289636664139174777
# 35323413594643452461575456357268656746837976785794
# 35722346434683345754579445686568155679767926678187
# 53476438526458754963756986517486719762859782187396
# 34253517434536462854564757396567586841767869795287
# 45332667135644377824675548893578665991468977611257
# 44961841755517295286662831639777394274188841538529
# 46246169155735727126684683823779579493488168151459
# 54698446526571955763768216687487932779859814388196
# 69373648937148475914825958612593616972361472718347
# 17967414442817852555392896366641391747775241285888
# 46434524615754563572686567468379767857948187896815
# 46833457545794456865681556797679266781878137789298
# 64587549637569865174867197628597821873961893298417
# 45364628545647573965675868417678697952878971816398
# 56443778246755488935786659914689776112579188722368
# 55172952866628316397773942741888415385299952649631
# 57357271266846838237795794934881681514599279262561
# 65719557637682166874879327798598143881961925499217
# 71484759148259586125936169723614727183472583829458
# 28178525553928963666413917477752412858886352396999
# 57545635726865674683797678579481878968159298917926
# 57944568656815567976792667818781377892989248891319
# 75698651748671976285978218739618932984172914319528
# 56475739656758684176786979528789718163989182927419
# 67554889357866599146897761125791887223681299833479

# The total risk of this path is 315 (the starting position is still never entered, so its risk is not counted).

# Using the full map, what is the lowest total risk of any path from the top left to the bottom right?


from typing import Dict, List


class MapThing:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.grid = dict()
        self.min_x = 0
        self.max_x = -1
        self.min_y = 0
        self.max_y = -1

    def print(self):
        """
        Just simple output..
        """
        print(f"MapThing {self.max_x-self.min_x + 1}x{self.max_y - self.min_y + 1}")
        for y in range(self.min_y, self.max_y + 1):
            s = ""
            for x in range(self.min_x, self.max_x + 1):
                s += str(self.grid[(x, y)])
            print(s)

    def scale(self, x_scale, y_scale):
        """
        Scale up the cavern using the part2 logic
        """
        # grab the existing grid as a template
        existing_grid = self.grid
        # and calculate the width and height
        grid_width = self.max_x - self.min_x + 1
        grid_height = self.max_y - self.min_y + 1

        # reset to clean
        self.reset()

        # multiply out each location
        for location, base_danger in existing_grid.items():
            base_x, base_y = location
            for x_mul in range(x_scale):
                for y_mul in range(y_scale):
                    this_x = base_x + grid_width * x_mul
                    this_y = base_y + grid_height * y_mul
                    this_danger = base_danger + x_mul + y_mul
                    while this_danger > 9:
                        this_danger -= 9
                    self.store_danger(this_x, this_y, this_danger)

    def store_danger(self, x: int, y: int, danger_level: int):
        """
        Add this to the map
        """
        self.grid[(x, y)] = danger_level
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def load_file(self, filename: str):
        """
        Load the map from the file
        """
        with open(filename, "r") as f:
            y = 0
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    for x, the_val in enumerate(this_line):
                        self.store_danger(x, y, int(the_val))
                    y += 1

    def neighbours_of(x: int, y: int):
        result = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return result

    def score_all_routes(self):
        """
        New approach, we start with an empty grid except for the bottom right
        That bottom right has its own score.

        Each location will hold the total risk to get to the end including itself
        Each iteration we can see whether any location has a better neighbour to get to the end.
        Once we have a run with no improvements we should have the truth
        """

        # Start it off with a single seed
        risk_from_here = dict()
        risk_from_here[(self.max_x, self.max_y)] = self.grid[(self.max_x, self.max_y)]

        # loop until we have no improvements
        modified = True
        mod_loops = 0
        while modified:
            # Fresh iteration
            modified = False

            # ideally loop backwards to reduce the initial lops required
            for y in range(self.max_y, self.min_y - 1, -1):
                for x in range(self.max_x, self.min_x - 1, -1):
                    key = (x, y)
                    # get all the neighbours' scores
                    neighbours = [
                        risk_from_here[l]
                        for l in MapThing.neighbours_of(x, y)
                        if l in risk_from_here
                    ]
                    # get the best neighbour score
                    if 0 != len(neighbours):
                        best_neighbour = min(neighbours)
                        best_total = best_neighbour + self.grid[key]
                        if (
                            key not in risk_from_here
                            or best_total < risk_from_here[key]
                        ):
                            risk_from_here[key] = best_total
                            modified = True
            mod_loops += 1

        # and we're done
        print(f"score_all_routes: {mod_loops} modification loops")
        # select the smaller risk-from-here value..
        risk_starting_down = risk_from_here[(0, 1)]
        risk_starting_right = risk_from_here[(1, 0)]

        lowest_risk = min(risk_starting_down, risk_starting_right)

        return lowest_risk

    def find_safest(
        self,
        x: int,
        y: int,
        steps_so_far: List,
        danger_so_far: int,
        best_path_record: Dict,
    ):
        """
        The recursive wandering chunk..
        """
        key = (x, y)

        # 0) Are we off the grid ?
        if key not in self.grid:
            return

        this_danger = danger_so_far + self.grid[key]

        # and are we just wating our time ?
        if this_danger >= self.best_danger:
            return

        # 1) Check whether we've been here before or better
        if key in best_path_record:
            if best_path_record[key] < this_danger:
                # we have already been here more efficiently, we're done..
                return

        # 2) Check we haven't been here before..
        # Actually, this is probably impossible..
        # going to assert that's the case and figure it out later if not..
        # assert key not in steps_so_far

        # 3) ok, we should do work from here..
        best_path_record[key] = this_danger
        steps_so_far.append(key)

        # 4) Was this the final step ?
        if self.max_x == x and self.max_y == y:
            print(f"Storing a final path with danger {this_danger} : {steps_so_far}")
            self.best_danger = this_danger
        else:
            # We can now move out and try all the different directions..
            self.find_safest(x + 1, y, steps_so_far, this_danger, best_path_record)
            self.find_safest(x, y + 1, steps_so_far, this_danger, best_path_record)
            self.find_safest(x - 1, y, steps_so_far, this_danger, best_path_record)
            self.find_safest(x, y - 1, steps_so_far, this_danger, best_path_record)

        # 5) and allow recursion to be cool..
        steps_so_far.pop()
        return

    def calculate_safest_route(self):
        """
        Calculate the safest route to the bottom right of the map
        start at the top-left
        """
        # basic plan, go right, go down, go left, go up
        # if we have been to a location more efficiently then we can stop
        # if we have reached the end more safely than our current move then
        # also time to stop.
        # shortest route should end quite quickly (maybe)
        self.best_danger = 9999999999
        current_x = self.min_x
        current_y = self.min_y

        steps_so_far = [(current_x, current_y)]
        danger_so_far = 0  # no danger for the first step..
        best_path_record = dict()  # no idea what the best path to anywhere is so far..

        # first try going right..
        self.find_safest(
            current_x + 1, current_y, steps_so_far, danger_so_far, best_path_record
        )

        # and now try starting down..
        self.find_safest(
            current_x, current_y + 1, steps_so_far, danger_so_far, best_path_record
        )

        # and we're done.. what's the most efficient to the bottom right ?

        return self.best_danger


def part1(filename: str) -> int:
    """
    Run the part1 solution
    """
    cavern = MapThing()
    cavern.load_file(filename)
    cavern.print()
    safest_route = cavern.score_all_routes()

    return safest_route


def part2(filename: str) -> int:
    """
    Run the part2 solution
    """
    cavern = MapThing()
    cavern.load_file(filename)
    cavern.print()
    cavern.scale(5, 5)
    cavern.print()
    safest_route = cavern.score_all_routes()

    return safest_route


if __name__ == "__main__":
    test_filename = "test_input.txt"
    puzzle_filename = "puzzle_input.txt"
    test1_expected = 40
    part1_expected = 403
    test2_expected = 315

    test1 = part1(test_filename)
    print(f"Test part1 returned {test1}, should have been {test1_expected}")
    assert test1 == test1_expected

    puzz1 = part1(puzzle_filename)
    print(f"Part1 actual result : {puzz1}, should be {part1_expected}")
    assert puzz1 == part1_expected

    test2 = part2(test_filename)
    print(f"Test part2 returned {test2}, should have been {test2_expected}")
    assert test2 == test2_expected

    puzz2 = part2(puzzle_filename)
    print(f"Part2 actual result : {puzz2}")
