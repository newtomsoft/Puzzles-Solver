from PuzzleSolver.Puzzles.KinKonKan.KinKonKanSolver import KinKonKanSolver
from GridPlayers.GridPuzzle.GridPuzzleKinKonKanPlayer import GridPuzzleKinKonKanPlayer
from GridProviders.GridPuzzle.GridPuzzleKinKonKanGridProvider import GridPuzzleKinKonKanGridProvider
from Run.GameRegistry import GameRegistry

def register():
    GameRegistry.register(
        r"https://gridpuzzle.com/kin-kon-kan.*", 
        GridPuzzleKinKonKanGridProvider, 
        GridPuzzleKinKonKanPlayer
    )(KinKonKanSolver)
