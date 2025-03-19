from Utils.Direction import Direction


class Pipe:
    def __init__(self, input_string: str):
        if len(input_string) != 2:
            raise ValueError("Invalid pipe shape string")
        if input_string[0] not in ["L", "I", "T", "E"]:
            raise ValueError("Invalid pipe shape letter")
        if not input_string[1].isdigit() or int(input_string[1]) < 0 or int(input_string[1]) > 3:
            raise ValueError("Invalid pipe shape rotation")

        self._input_string = input_string
        self.counterclockwise_rotation = int(input_string[1])
        self.clockwise_rotation = (4 - self.counterclockwise_rotation) % 4

        match input_string[0]:
            case "L":
                self.shape = "L"
            case "I":
                self.shape = "I"
            case "T":
                self.shape = "T"
            case "E":
                self.shape = "E"

    def __str__(self):
        match self.shape, self.counterclockwise_rotation:
            case "L", 0:
                return ' └─'
            case "L", 1:
                return '─┘ '
            case "L", 2:
                return '─┐ '
            case "L", 3:
                return ' ┌─'
            case "I", 0:
                return ' │ '
            case "I", 1:
                return '───'
            case "T", 0:
                return '─┬─'
            case "T", 1:
                return ' ├─'
            case "T", 2:
                return '─┴─'
            case "T", 3:
                return '─┤ '
            case "E", 0:
                return ' ╶─'
            case "E", 1:
                return ' ╵ '
            case "E", 2:
                return '─╴ '
            case "E", 3:
                return ' ╷ '
            case _:
                raise ValueError("Invalid pipe shape")

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_connection(up: bool = False, down: bool = False, left: bool = False, right: bool = False):
        match (up, right, down, left):
            case (True, True, False, False): return Pipe("L0")
            case (True, False, False, True): return Pipe("L1")
            case (False, False, True, True): return Pipe("L2")
            case (False, True, True, False): return Pipe("L3")

            case (True, False, True, False): return Pipe("I0")
            case (False, True, False, True): return Pipe("I1")

            case (False, True, True, True): return Pipe("T0")
            case (True, True, True, False): return Pipe("T1")
            case (True, True, False, True): return Pipe("T2")
            case (True, False, True, True): return Pipe("T3")

            case (False, True, False, False): return Pipe("E0")
            case (True, False, False, False): return Pipe("E1")
            case (False, False, False, True): return Pipe("E2")
            case (False, False, True, False): return Pipe("E3")

            case _: raise ValueError("Invalid pipe shape")

    def get_open_to(self) -> dict[Direction, bool]:
        match self.shape, self.counterclockwise_rotation:
            case "L", 0:
                return {Direction.up(): True, Direction.down(): False, Direction.left(): False, Direction.right(): True}
            case "L", 1:
                return {Direction.up(): True, Direction.down(): False, Direction.left(): True, Direction.right(): False}
            case "L", 2:
                return {Direction.up(): False, Direction.down(): True, Direction.left(): True, Direction.right(): False}
            case "L", 3:
                return {Direction.up(): False, Direction.down(): True, Direction.left(): False, Direction.right(): True}

            case "I", 0:
                return {Direction.up(): True, Direction.down(): True, Direction.left(): False, Direction.right(): False}
            case "I", 1:
                return {Direction.up(): False, Direction.down(): False, Direction.left(): True, Direction.right(): True}

            case "T", 0:
                return {Direction.up(): False, Direction.down(): True, Direction.left(): True, Direction.right(): True}
            case "T", 1:
                return {Direction.up(): True, Direction.down(): True, Direction.left(): False, Direction.right(): True}
            case "T", 2:
                return {Direction.up(): True, Direction.down(): False, Direction.left(): True, Direction.right(): True}
            case "T", 3:
                return {Direction.up(): True, Direction.down(): True, Direction.left(): True, Direction.right(): False}

            case "E", 0:
                return {Direction.up(): False, Direction.down(): False, Direction.left(): False, Direction.right(): True}
            case "E", 1:
                return {Direction.up(): True, Direction.down(): False, Direction.left(): False, Direction.right(): False}
            case "E", 2:
                return {Direction.up(): False, Direction.down(): False, Direction.left(): True, Direction.right(): False}
            case "E", 3:
                return {Direction.up(): False, Direction.down(): True, Direction.left(): False, Direction.right(): False}

            case _:
                raise ValueError("Invalid pipe shape")

    @staticmethod
    def from_repr(shape_repr: str):
        match shape_repr:
            case ' └─': return Pipe("L0")
            case '─┘ ': return Pipe("L1")
            case '─┐ ': return Pipe("L2")
            case ' ┌─': return Pipe("L3")
            case ' │ ': return Pipe("I0")
            case '───': return Pipe("I1")
            case '─┬─': return Pipe("T0")
            case ' ├─': return Pipe("T1")
            case '─┴─': return Pipe("T2")
            case '─┤ ': return Pipe("T3")
            case ' ╶─': return Pipe("E0")
            case ' ╵ ': return Pipe("E1")
            case '─╴ ': return Pipe("E2")
            case ' ╷ ': return Pipe("E3")
            case _: raise ValueError("Invalid shape representation")
