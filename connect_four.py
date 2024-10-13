from typing import List


Grid = List[List[str]]

def height(grid: Grid) -> int:
    max_num = 0

    for element in grid:
        if len(element) > max_num:
            max_num = len(element)

    return max_num


def edge_line(grid: Grid) -> str:
    result = ''

    for _ in range(len(grid)):
        result += '+---'

    return (result + '+')


def center_line(grid: Grid, row_num: int) -> str:
    result = ''

    for index in range(len(grid)):
        if len(grid[index]) > row_num:
            result += '| ' + grid[index][row_num] + ' '
        else:
            result += "|   "

    return (result + '|')


def num_line(grid: Grid) -> str:
    result = ''

    for index in range(len(grid)):
        result += '  ' + str(index) + ' '

    return result


def draw(grid: Grid) -> None:
    row_num = height(grid) - 1

    for _ in range(height(grid)):
        print(edge_line(grid))
        print(center_line(grid, row_num))
        row_num -= 1

    print(edge_line(grid))
    print(num_line(grid))

def is_vertical(grid: Grid, player: str, column: int) -> bool:
    if len(grid[column]) <= 3:
        return False

    for index in range(-1, -5, -1):
        if grid[column][index] != player:
            return False

    return True


def frame_diag_hor(grid: Grid, player: str, column: int, row: int,
                   step: int) -> bool:
    count = 0
    max_height = height(grid)

    for index in range(column - 4, column + 5):
        if index >= 0 and index < len(grid) and row > 0 and row <= max_height\
           and len(grid[index]) >= row and grid[index][row - 1] == player:
            count += 1
        else:
            if count == 4:
                return True

            count = 0
        row = row + step

    return False


def play(grid: Grid, player: str, column: int) -> bool:
    grid[column].append(player)
    return is_vertical(grid, player, column) or\
        frame_diag_hor(grid, player, column, len(grid[column]), 0) or\
        frame_diag_hor(grid, player, column, len(grid[column]) - 4, 1) or\
        frame_diag_hor(grid, player, column, len(grid[column]) + 4, -1)


def main() -> None:
    grid: Grid = [['X'], [], ['O', 'X'], [], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'X', 3)
    assert grid == [['X'], [], ['O', 'X'], ['X'], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'O', 3)
    assert grid == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], [], []]

    assert not play(grid, 'X', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], ['X'], []]

    assert not play(grid, 'O', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'], ['X', 'O', 'O'], ['X', 'O'], []]

    assert not play(grid, 'X', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'],
            ['X', 'O', 'O'], ['X', 'O', 'X'], []]

    assert play(grid, 'O', 5)
    assert grid \
        == [['X'], [], ['O', 'X'], ['X', 'O'],
            ['X', 'O', 'O'], ['X', 'O', 'X', 'O'], []]


def run_game(size: int) -> None:
    player = 'O'
    grid: Grid = [[] for _ in range(size)]
    draw(grid)
    over = False
    while not over:
        player = 'X' if player == 'O' else 'O'
        column = int(input("\nPlayer " + player + ": "))
        print()
        over = play(grid, player, column)
        draw(grid)
    print("\nGame over, player", player, "won.")


if __name__ == '__main__':
    main()
#    run_game(10)  # uncomment to play the game
