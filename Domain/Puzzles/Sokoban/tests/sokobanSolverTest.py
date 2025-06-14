import unittest
from unittest import TestCase

from Domain.Puzzles.Sokoban.sokobanSolver import recherche_solution


class SokobanSolverTest(TestCase):
    def test_solution_0(self):
        grid = (
            '######\n'
            '#.   #\n'
            '## $ #\n'
            '#@.$ #\n'
            '######'
        )
        step_count = recherche_solution(grid, 20)
        self.assertEqual(13, step_count)

    def test_solution_1(self):
        grid = (
            '  ###   \n'
            '  #.#   \n'
            '  # ####\n'
            '###$ $.#\n'
            '#. $@###\n'
            '####$#  \n'
            '   #.#  \n'
            '   ###  '
        )
        step_count = recherche_solution(grid, 20)
        self.assertEqual(10, step_count)

    def test_solution_2(self):
        grid = (
            '######\n'
            '##.$.#\n'
            '#  # #\n'
            '# $$ #\n'
            '#.  @#\n'
            '######'
        )
        step_count = recherche_solution(grid, 25)
        self.assertNotEqual(21, step_count)

    def test_solution_3(self):
        grid = (
            '#####\n'
            '#   #\n'
            '# #$#\n'
            '# $ #\n'
            '#@$.#\n'
            '#.#.#\n'
            '#####'
        )
        step_count = recherche_solution(grid, 26)
        self.assertEqual(19, step_count)

    def test_solution_4(self):
        grid = (
            '#######\n'
            '#  .$ #\n'
            '#     #\n'
            '## # ##\n'
            ' #$@.##\n'
            ' #   ##\n'
            ' ######'
        )
        step_count = recherche_solution(grid, 50)
        self.assertEqual(44, step_count)

    def test_solution_40(self):
        grid = (
            ' #######  \n'
            ' #     ###\n'
            '##$###   #\n'
            '# @ $  $ #\n'
            '# ..# $ ##\n'
            '##..#   # \n'
            ' ######## '
        )
        step_count = recherche_solution(grid, 120)
        self.assertEqual(114, step_count)

    def test_solution_str_01(self):
        grid_str = (
            '  #######\n'
            '###     #\n'
            '# $ $   #\n'
            '# ### #####\n'
            '# @ . .   #\n'
            '#   ###   #\n'
            '##### #####'
        )
        step_count = recherche_solution(grid_str, 500)
        self.assertEqual(False, step_count)

    def test_solution_str_02(self):
        grid_str = (
            '  ####   \n'
            '###  ####\n'
            '#       #\n'
            '#@$***. #\n'
            '#       #\n'
            '#########'
        )
        step_count = recherche_solution(grid_str, 100)
        self.assertEqual(30, step_count)

    def test_solution_str_03(self):
        grid_str = (
            '#######\n'
            '#. #  #\n'
            '#  $  #\n'
            '#. $#@#\n'
            '#  $  #\n'
            '#. #  #\n'
            '#######'
        )
        step_count = recherche_solution(grid_str, 100)
        self.assertEqual(41, step_count)

    def test_solution_str_31(self):
        grid_str = (
            '  #### \n'
            ' ##  # \n'
            '##@$.##\n'
            '# $$  #\n'
            '# . . #\n'
            '###   #\n'
            '  #####'
        )
        step_count = recherche_solution(grid_str, 100)
        self.assertEqual(17, step_count)

    def test_solution_str_32(self):
        grid_str = (
            ' ####  \n'
            '##  ###\n'
            '#     #\n'
            '#.**$@#\n'
            '#   ###\n'
            '##  #  \n'
            ' ####  '
        )
        step_count = recherche_solution(grid_str, 100)
        self.assertEqual(35, step_count)

    def test_solution_soko01(self):
        grid_str = (
            '      ###      \n'
            '      #.#      \n'
            '  #####.#####  \n'
            ' ##         ## \n'
            '##  # # # #  ##\n'
            '#  ##     ##  #\n'
            '# ##  # #  ## #\n'
            '#     $@$     #\n'
            '####  ###  ####\n'
            '   #### ####   '
        )
        step_count = recherche_solution(grid_str, 100)
        self.assertEqual(78, step_count)

    @unittest.skip("Too long")
    def test_solution_soko02(self):
        grid_str = (
            ' ###########     \n'
            '##         ##    \n'
            '#  $     $  #    \n'
            '# $# #.# #$ #    \n'
            '#    #*#    #####\n'
            '#  ###.###  #   #\n'
            '#  .*.@.*.      #\n'
            '#  ###.###  #   #\n'
            '#    #*#    #####\n'
            '# $# #.# #$ #    \n'
            '#  $     $  #    \n'
            '##         ##    \n'
            ' ###########     '
        )
        step_count = recherche_solution(grid_str, 200)
        self.assertEqual(146, step_count)

    @unittest.skip("Too long")
    def test_solution_soko03(self):
        grid_str = (
            '     #####     \n'
            '    ##   #     \n'
            '    #    #     \n'
            '  ###    ######\n'
            '  #.#.# ##.   #\n'
            '### ###  ##   #\n'
            '#   #  $  ## ##\n'
            '#     $@$     #\n'
            '#   #  $  #   #\n'
            '######   ### ##\n'
            ' #  .## #### # \n'
            ' #           # \n'
            ' ##  ######### \n'
            '  ####         '
        )
        step_count = recherche_solution(grid_str, 90)
        self.assertEqual(83, step_count)

    @unittest.skip("Too long")
    def test_solution_soko04(self):
        grid_str = (
            '     #####     \n'
            '    ##   ##    \n'
            '  ### $ $ ###  \n'
            ' ##   # #   ## \n'
            '##           ##\n'
            '# $#  ... #$  #\n'
            '#     .@.     #\n'
            '#  $# ...  #$ #\n'
            '##           ##\n'
            ' ##   # #   ## \n'
            '  ### $ $ ###  \n'
            '    ##   ##    \n'
            '     #####     '
        )
        step_count = recherche_solution(grid_str, 105)
        self.assertEqual(102, step_count)

    @unittest.skip("Too long")
    def test_solution_soko06(self):
        grid_str = (
            '     #     #     \n'
            '    #########    \n'
            '     #     #     \n'
            '   ###     ###   \n'
            ' # # #     # # # \n'
            '###### #.# ######\n'
            ' #    $. .$    # \n'
            ' #   # #$# #   # \n'
            ' #   . $@$ .   # \n'
            ' #   # #$# #   # \n'
            ' #    $. .$    # \n'
            '###### #.# ######\n'
            ' # # #     # # # \n'
            '   ###     ###   \n'
            '     #     #     \n'
            '    #########    \n'
            '     #     #     '
        )
        step_count = recherche_solution(grid_str, 60)
        self.assertEqual(52, step_count)

    def test_solution_3454(self):
        # http://www.game-sokoban.com/index.php?mode=level&lid=3454
        grid_str = (
            '######        \n'
            '#   .######## \n'
            '#@*  ##     ##\n'
            '##$#### ###  #\n'
            ' #           #\n'
            ' # #### ### ##\n'
            ' # ###  # # # \n'
            ' # #   #### # \n'
            ' # #        # \n'
            '## ## ####  # \n'
            '#  ## #  #### \n'
            '#     #       \n'
            '####  #       \n'
            '   ####       '
        )
        step_count = recherche_solution(grid_str, 150)
        self.assertEqual(146, step_count)

    @unittest.skip("Too long")
    def test_solution_16457(self):
        #  http://www.game-sokoban.com/index.php?mode=level&lid=16457
        grid_str = (
            '##########\n'
            '#.       #\n'
            '#...  .. #\n'
            '# ###@####\n'
            '#      $ #\n'
            '# $$ $ # #\n'
            '#  $$##  #\n'
            '##      ##\n'
            ' ######## '
        )
        step_count = recherche_solution(grid_str, 180)
        self.assertEqual(176, step_count)
