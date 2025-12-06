from Domain.Puzzles.Grades.GradesSolver import GradesSolver
from GridPlayers.GridPuzzle.GridPuzzleGradesPlayer import GridPuzzleGradesPlayer
from GridProviders.GridPuzzle.GridPuzzleGradesGridProvider import GridPuzzleGradesGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/grades", 
        GridPuzzleGradesGridProvider, 
        GridPuzzleGradesPlayer
    )(GradesSolver)