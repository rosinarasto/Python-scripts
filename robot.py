from typing import Dict, Set, Tuple, Optional


Heading = int
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
Tile = Set[Heading]

Position = Tuple[int, int]
Plan = Dict[Position, Tile]


def frame_of_check(plan: Plan, key: Position, direction: int) -> bool:
    x, y = key
    x_shift, y_shift = shift_by(direction, x, y)

    return (x_shift, y_shift) in plan and \
           (direction + 2) % 4 in plan[(x_shift, y_shift)] and \
           direction in plan[(x, y)]


def shift_by(call: int, x: int, y: int) -> Position:
    if call == NORTH:
        y -= 1
    if call == EAST:
        x += 1
    if call == SOUTH:
        y += 1
    if call == WEST:
        x -= 1

    return (x, y)


def is_correct(plan: Plan) -> bool:

    for x, y in plan.keys():

        for elem in plan[(x, y)]:
            x_shift, y_shift = shift_by(elem, x, y)

            if (x_shift, y_shift) not in plan or (elem + 2) % 4 not in plan[(x_shift, y_shift)]:
                return False

    return True

Step = Optional[Tuple[int, int, int]]


def step(call: int, plan: Plan, x: int, y: int) -> Step:
    if call == NORTH and frame_of_check(plan, (x, y), NORTH):
        return (x, y - 1, NORTH)

    if call == EAST and frame_of_check(plan, (x, y), EAST):
        return (x + 1, y, EAST)

    if call == SOUTH and frame_of_check(plan, (x, y), SOUTH):
        return (x, y + 1, SOUTH)

    if call == WEST and frame_of_check(plan, (x, y), WEST):
        return (x - 1, y, WEST)

    return None


def run(plan: Plan, start: Position) -> Position:
    (x, y) = start
    direction = 3

    for elem in plan[start]:
        if elem < direction:
            direction = elem

    visited: Set[Position] = set()
    visited.add(start)

    while plan.keys():
        (x_shift, y_shift) = (x, y)

        for i in range(3):
            direction = (direction + i) % 4
            if step(direction, plan, x, y) is not None:
                x_shift, y_shift = shift_by(direction, x, y)
                break

        if (x_shift, y_shift) in visited or \
           (x, y) == (x_shift, y_shift):
            return (x_shift, y_shift)

        visited.add((x, y))
        (x, y) = (x_shift, y_shift)

    assert False


def main() -> None:
    assert is_correct({})
    assert is_correct({(1, 1): set()})
    assert is_correct({(1, 1): {NORTH}, (1, 0): {SOUTH}})
    assert is_correct({
        (3, 3): {NORTH, WEST},
        (2, 2): {SOUTH, EAST},
        (3, 2): {SOUTH, WEST},
        (2, 3): {NORTH, EAST},
    })

    assert not is_correct({(7, 7): {WEST}})
    assert not is_correct({(7, 7): {WEST}, (6, 7): set()})
    assert not is_correct({
        (3, 3): {NORTH, WEST},
        (2, 2): {SOUTH, EAST},
        (3, 2): {SOUTH, WEST},
        (2, 3): {NORTH},
    })

    plan = {
        (-2, -2): {EAST, SOUTH},
        (-1, -2): {EAST, WEST},
        (0, -2): {SOUTH, WEST},
        (-5, -1): {SOUTH},
        (-2, -1): {NORTH, SOUTH},
        (0, -1): {NORTH, SOUTH},
        (5, -1): {EAST, SOUTH},
        (6, -1): {SOUTH, WEST},
        (-5, 0): {NORTH, EAST, SOUTH},
        (-4, 0): {EAST, WEST},
        (-3, 0): {EAST, WEST},
        (-2, 0): {NORTH, EAST, WEST},
        (-1, 0): {EAST, WEST},
        (0, 0): {NORTH, EAST, SOUTH, WEST},
        (1, 0): {EAST, WEST},
        (2, 0): {EAST, SOUTH, WEST},
        (3, 0): {EAST, WEST},
        (4, 0): {EAST, WEST},
        (5, 0): {NORTH, EAST, WEST},
        (6, 0): {NORTH, WEST},
        (-5, 1): {NORTH},
        (0, 1): {NORTH, SOUTH},
        (2, 1): {NORTH, SOUTH},
        (-1, 2): {EAST},
        (0, 2): {NORTH, EAST, WEST},
        (1, 2): {EAST, WEST},
        (2, 2): {NORTH, WEST},
    }

    assert run({(0, 0): set()}, (0, 0)) == (0, 0)
    assert run({(1, 1): {NORTH}, (1, 0): {SOUTH}}, (1, 1)) == (1, 0)
    assert run({(1, 1): {NORTH}, (1, 0): {SOUTH}}, (1, 0)) == (1, 1)

    assert is_correct(plan)

    assert run(plan, (0, 0)) == (-5, -1)
    assert run(plan, (-5, -1)) == (-5, 1)
    assert run(plan, (-4, 0)) == (5, 0)
    assert run(plan, (0, 1)) == (-5, -1)
    assert run(plan, (-1, 2)) == (5, 0)

    plan[2, 0] = {WEST, SOUTH}
    plan[3, 0] = {EAST}

    assert is_correct(plan)

    assert run(plan, (-4, 0)) == (-1, 2)
    assert run(plan, (1, 2)) == (-5, -1)


if __name__ == '__main__':
    main()
