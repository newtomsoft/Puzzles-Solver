from Domain.Puzzles.Str8ts.Str8tsSolver import Str8tsSolver
from GridPlayers.GridPuzzle.GridPuzzleStr8tsPlayer import GridPuzzleStr8tsPlayer
from GridProviders.GridPuzzle.GridPuzzleStr8tsGridProvider import GridPuzzleStr8tsGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/str8ts", 
        GridPuzzleStr8tsGridProvider, 
        GridPuzzleStr8tsPlayer
    )(Str8tsSolver)