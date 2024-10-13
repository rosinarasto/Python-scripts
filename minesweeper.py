from typing import Dict, Tuple, Set


Position = Tuple[int, int]


class Minesweeper:
    def __init__(self, width: int, height: int,
                 mines: Dict[Position, int]):
        self.mines = mines
        self.score = 0
        self.width = width
        self.height = height
        self.status = [[' ' for _ in range(width)] for _ in range(height)]

    def valid_position(self, x: int, y: int,
                       flag: bool, shift: int) -> Set[Position]:
        result: Set[Position] = set()

        for shift_y in range(max(0, y - shift), min(y + shift + 1, self.height)):

            for shift_x in range(max(0, x - shift), min(x + shift + 1, self.width)):
                if not flag or (flag and (shift_x, shift_y) in self.mines):
                    result.add((shift_x, shift_y))

        return result

    def bomb_reveal(self, x: int, y: int) -> None:
        self.score -= 10
        self.status[y][x] = '*'
        valid = self.valid_position(x, y, False, self.mines[(x, y)])

        for shift_x, shift_y in valid:
            if self.status[shift_y][shift_x] == '*':
                continue

            if (shift_x, shift_y) in self.mines:
                self.bomb_reveal(shift_x, shift_y)
            else:
                self.status[shift_y][shift_x] = 'X'

    def number_reveal(self, x: int, y: int) -> None:
        self.score += 1
        self.status[y][x] = str(len(self.valid_position(x, y, True, 1)))
        if self.status[y][x] != '0':
            return

        valid = self.valid_position(x, y, False, 1)

        for shift_x, shift_y in valid:
            if self.status[shift_y][shift_x] != ' ':
                continue

            self.number_reveal(shift_x, shift_y)

    def uncover(self, x: int, y: int) -> None:
        if self.status[y][x] == ' ':
            if (x, y) not in self.mines:
                self.number_reveal(x, y)
            else:
                self.bomb_reveal(x, y)


def main() -> None:
    mines = {(2, 2): 5, (4, 5): 1, (6, 1): 0, (6, 3): 1, (6, 4): 3}

    ms = Minesweeper(8, 6, mines)
    assert ms.score == 0
    assert ms.status == [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(1, 1)
    assert ms.score == 1
    assert ms.status == [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(0, 0)
    assert ms.score == 33
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', '1', '1', '3', ' ', ' '],
        ['0', '0', '0', '1', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(5, 4)
    assert ms.score == 33
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', '1', '1', '3', ' ', ' '],
        ['0', '0', '0', '1', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(4, 5)
    assert ms.score == 23
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', 'X', 'X', 'X', ' ', ' '],
        ['0', '0', '0', 'X', '*', 'X', ' ', ' '],
    ]

    ms.uncover(5, 5)
    assert ms.score == 23
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', 'X', 'X', 'X', ' ', ' '],
        ['0', '0', '0', 'X', '*', 'X', ' ', ' '],
    ]

    ms.uncover(6, 3)
    assert ms.score == -7
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', 'X', 'X', 'X', '*', 'X'],
        ['0', '1', ' ', 'X', 'X', 'X', 'X', 'X'],
        ['0', '1', '1', 'X', 'X', 'X', '*', 'X'],
        ['0', '0', '0', 'X', 'X', 'X', '*', 'X'],
        ['0', '0', '0', 'X', '*', 'X', 'X', 'X'],
    ]

    assert mines == {(2, 2): 5, (4, 5): 1, (6, 1): 0, (6, 3): 1, (6, 4): 3}


if __name__ == '__main__':
    main()
