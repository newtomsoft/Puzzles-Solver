from Domain.Puzzles.No4InARow.No4InARowSolver import No4InARowSolver
from GridPlayers.GridPuzzle.GridPuzzleNo4InARowPlayer import GridPuzzleNo4InARowPlayer
from GridProviders.GridPuzzle.GridPuzzleNo4InARowGridProvider import GridPuzzleNo4InARowGridProvider
from Run.GameRegistry import GameRegistry


def register():
    GameRegistry.register(
        r"https://.*gridpuzzle\.com/no-four-in-row", 
        GridPuzzleNo4InARowGridProvider, 
        GridPuzzleNo4InARowPlayer
    )(No4InARowSolver)