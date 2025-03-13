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

        if input_string[0] == "L":
            self.shape = "L"
            return
        if input_string[0] == "I":
            self.shape = "I"
            return
        if input_string[0] == "T":
            self.shape = "T"
            return
        if input_string[0] == "E":
            self.shape = "E"

    def __str__(self):
        if self.shape == "L" and self.counterclockwise_rotation == 0:
            return ' └─'
        if self.shape == "L" and self.counterclockwise_rotation == 1:
            return '─┘ '
        if self.shape == "L" and self.counterclockwise_rotation == 2:
            return '─┐ '
        if self.shape == "L" and self.counterclockwise_rotation == 3:
            return ' ┌─'
        if self.shape == "I" and self.counterclockwise_rotation == 0:
            return ' │ '
        if self.shape == "I" and self.counterclockwise_rotation == 1:
            return '───'
        if self.shape == "T" and self.counterclockwise_rotation == 0:
            return '─┬─'
        if self.shape == "T" and self.counterclockwise_rotation == 1:
            return ' ├─'
        if self.shape == "T" and self.counterclockwise_rotation == 2:
            return '─┴─'
        if self.shape == "T" and self.counterclockwise_rotation == 3:
            return '─┤ '
        if self.shape == "E" and self.counterclockwise_rotation == 0:
            return ' ╶─'
        if self.shape == "E" and self.counterclockwise_rotation == 1:
            return ' ╵ '
        if self.shape == "E" and self.counterclockwise_rotation == 2:
            return '─╴ '
        if self.shape == "E" and self.counterclockwise_rotation == 3:
            return ' ╷ '
        raise ValueError("Invalid pipe shape")

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_connection(up: bool = False, down: bool = False, left: bool = False, right: bool = False):
        if up and down and left and right:
            raise ValueError("Invalid pipe shape (all connections are True)")
        if not up and not down and not left and not right:
            raise ValueError("Invalid pipe shape (all connections are False)")

        if up and right and not down and not left:
            return Pipe("L0")
        if left and up and not right and not down:
            return Pipe("L1")
        if down and left and not up and not right:
            return Pipe("L2")
        if right and down and not up and not left:
            return Pipe("L3")

        if up and down and not left and not right:
            return Pipe("I0")
        if left and right and not up and not down:
            return Pipe("I1")

        if left and right and down and not up:
            return Pipe("T0")
        if up and down and right and not left:
            return Pipe("T1")
        if up and right and left and not down:
            return Pipe("T2")
        if up and down and left and not right:
            return Pipe("T3")

        if right and not down and not left and not up:
            return Pipe("E0")
        if up and not down and not right and not left:
            return Pipe("E1")
        if left and not right and not up and not down:
            return Pipe("E2")
        if down and not up and not left and not right:
            return Pipe("E3")

        raise ValueError("Invalid pipe shape")

    def get_open_to(self) -> dict[Direction, bool]:
        if self.shape == "L" and self.counterclockwise_rotation == 0:
            return {Direction.up(): True, Direction.down(): False, Direction.left(): False, Direction.right(): True}
        if self.shape == "L" and self.counterclockwise_rotation == 1:
            return {Direction.up(): True, Direction.down(): False, Direction.left(): True, Direction.right(): False}
        if self.shape == "L" and self.counterclockwise_rotation == 2:
            return {Direction.up(): False, Direction.down(): True, Direction.left(): True, Direction.right(): False}
        if self.shape == "L" and self.counterclockwise_rotation == 3:
            return {Direction.up(): False, Direction.down(): True, Direction.left(): False, Direction.right(): True}

        if self.shape == "I" and self.counterclockwise_rotation == 0:
            return {Direction.up(): True, Direction.down(): True, Direction.left(): False, Direction.right(): False}
        if self.shape == "I" and self.counterclockwise_rotation == 1:
            return {Direction.up(): False, Direction.down(): False, Direction.left(): True, Direction.right(): True}

        if self.shape == "T" and self.counterclockwise_rotation == 0:
            return {Direction.up(): False, Direction.down(): True, Direction.left(): True, Direction.right(): True}
        if self.shape == "T" and self.counterclockwise_rotation == 1:
            return {Direction.up(): True, Direction.down(): True, Direction.left(): False, Direction.right(): True}
        if self.shape == "T" and self.counterclockwise_rotation == 2:
            return {Direction.up(): True, Direction.down(): False, Direction.left(): True, Direction.right(): True}
        if self.shape == "T" and self.counterclockwise_rotation == 3:
            return {Direction.up(): True, Direction.down(): True, Direction.left(): True, Direction.right(): False}

        if self.shape == "E" and self.counterclockwise_rotation == 0:
            return {Direction.up(): False, Direction.down(): False, Direction.left(): False, Direction.right(): True}
        if self.shape == "E" and self.counterclockwise_rotation == 1:
            return {Direction.up(): True, Direction.down(): False, Direction.left(): False, Direction.right(): False}
        if self.shape == "E" and self.counterclockwise_rotation == 2:
            return {Direction.up(): False, Direction.down(): False, Direction.left(): True, Direction.right(): False}
        if self.shape == "E" and self.counterclockwise_rotation == 3:
            return {Direction.up(): False, Direction.down(): True, Direction.left(): False, Direction.right(): False}

        raise ValueError("Invalid pipe shape")

    @staticmethod
    def from_repr(shape_repr: str):
        shape_map = {
            ' └─': "L0",
            '─┘ ': "L1",
            '─┐ ': "L2",
            ' ┌─': "L3",
            ' │ ': "I0",
            '───': "I1",
            '─┬─': "T0",
            ' ├─': "T1",
            '─┴─': "T2",
            '─┤ ': "T3",
            ' ╶─': "E0",
            ' ╵ ': "E1",
            '─╴ ': "E2",
            ' ╷ ': "E3"
        }
        if shape_repr not in shape_map:
            raise ValueError("Invalid shape representation")
        return Pipe(shape_map[shape_repr])
