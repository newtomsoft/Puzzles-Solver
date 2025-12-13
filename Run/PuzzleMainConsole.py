from Run.GameComponentFactory import GameComponentFactory


class PuzzleMainConsole:
    @staticmethod
    def main():
        print("Puzzle Solver")
        print("Enter game url")
        url = input()

        match url:
            case "queens":
                url = "https://www.linkedin.com/games/queens"
            case "zip":
                url = "https://www.linkedin.com/games/zip"
            case "tango":
                url = "https://www.linkedin.com/games/tango"

        game_component_factory = GameComponentFactory()
        puzzle_runner = game_component_factory.create_game(url)
        puzzle_runner.run()


if __name__ == '__main__':
    PuzzleMainConsole.main()
