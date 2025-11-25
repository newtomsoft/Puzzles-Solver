from Domain.Puzzles.Vectors.VectorsSolver import VectorsSolver
from GridPlayers.PuzzleBaron.PuzzleBaronVectorsGridPlayer import PuzzleBaronVectorsPlayer
from GridProviders.PuzzleBaron.PuzzleBaronVectorsGridProvider import PuzzleBaronVectorsGridProvider
from Run.GameRegistry import GameRegistry


def register_vectors():
    GameRegistry.register_game(
        r"https://vectors\.puzzlebaron\.com/init2\.php", 
        PuzzleBaronVectorsGridProvider, 
        PuzzleBaronVectorsPlayer
    )(VectorsSolver)