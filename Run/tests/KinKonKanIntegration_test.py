import unittest
from unittest import TestCase

from Domain.Board.Grid import Grid
from Domain.Board.Direction import Direction
from Domain.Board.Position import Position
from Domain.Board.RegionsGrid import RegionsGrid
from Domain.Puzzles.KinKonKan.KinKonKanSolver import KinKonKanSolver

class KinKonKanIntegrationTest(TestCase):
    def test_solve_3x3_with_regions_grid(self):
        # Grille 3x3 avec 3 régions de 3 cellules
        # R0: (0,0), (0,1), (1,0)
        # R1: (0,2), (1,1), (1,2)
        # R2: (2,0), (2,1), (2,2)
        regions_matrix = [
            [0, 0, 1],
            [0, 1, 1],
            [2, 2, 2]
        ]
        regions_grid = RegionsGrid(regions_matrix)
        
        # Indices: A entre Top(0,0) et Right(2,2)
        indices = {
            'top': ['A', '', ''],
            'bottom': ['', '', ''],
            'left': ['', '', ''],
            'right': ['', '', 'A']
        }
        
        solver = KinKonKanSolver(regions_grid, indices)
        solution = solver.get_solution()
        
        self.assertIsNotNone(solution)
        # Vérifier qu'il y a un miroir par région
        regions_data = regions_grid.get_regions().values()
        for region in regions_data:
            mirrors = [solution[p.r][p.c] for p in region if solution[p.r][p.c] != '.']
            self.assertEqual(len(mirrors), 1)

if __name__ == '__main__':
    from Domain.Board.Grid import Grid
    from Domain.Board.Direction import Direction
    unittest.main()
