#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import copy
import pytest

# from . import util_copilot
# from . import util_gemini
from . import util_grok

# from . import util_deepseek
# from . import util_openai

PegsT = tuple[list[int], list[int], list[int]]
# PegsT = list[list]


def solve2(
    ndisks: int = 3,
    pegs: PegsT | type(None) = None,
    from_: int = 0,
    aux: int = 1,
    to: int = 2,
) -> Iterator[PegsT]:
    if pegs is None:
        pegs = [list(range(ndisks - 1, -1, -1)), [], []]
    yield from solve(pegs, ndisks, from_, aux, to)


def move_gpt(pegs: PegsT, from_: int, to: int) -> PegsT:
    disk = pegs[from_][-1]

    new_pegs = []
    for i, peg in enumerate(pegs):
        if i == from_:
            new_pegs.append(peg[:-1])
        elif i == to:
            new_pegs.append(peg + [disk])
        else:
            new_pegs.append(peg)

    return new_pegs


# move = move_gpt
# move = util_copilot.move
# move = util_gemini.move
# move = util_deepseek.move
# move = util_openai.move


def solve_gpt(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return

    # Phase 1: move n-1 to auxiliary
    current = pegs
    for state in solve(current, ndisks - 1, from_, to, aux):
        yield state
        current = state

    # Phase 2: move largest disk
    current = move(current, from_, to)
    yield current

    # Phase 3: move n-1 from auxiliary to target
    for state in solve(current, ndisks - 1, aux, from_, to):
        yield state
        current = state


# solve = solve_gpt
# solve = util_copilot.solve
# solve = util_gemini.solve
# solve = util_deepseek.solve
# solve = util_openai.solve


def move_vlz(pegs: PegsT, from_: int, to: int) -> PegsT:
    pegs = [list(p) for p in pegs]
    disk = pegs[from_].pop()
    pegs[to].append(disk)
    return pegs


def solve_vlz(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return pegs
    pegs = yield from solve(pegs, ndisks - 1, from_, to, aux)
    pegs = move(pegs, from_, to)
    yield pegs
    pegs = yield from solve(pegs, ndisks - 1, aux, from_, to)
    return pegs


move = move_vlz
solve = solve_vlz
# move = util_grok.move
# solve = util_grok.solve


@pytest.mark.parametrize(
    "ndisks, expected",
    [
        (1, [0]),
        (2, [1, 0]),
        (3, [2, 1, 0]),
        (4, [3, 2, 1, 0]),
        (5, [4, 3, 2, 1, 0]),
        (6, [5, 4, 3, 2, 1, 0]),
        (7, [6, 5, 4, 3, 2, 1, 0]),
        (8, [7, 6, 5, 4, 3, 2, 1, 0]),
    ],
)
def test_solve(ndisks, expected):
    pegs = [list(range(ndisks - 1, -1, -1)), [], []]
    result = solve(pegs, ndisks)
    result = list(result)[-1][2]
    print(f"{pegs = }, {expected = }, {result = }")
    assert result == expected


def test_functional_solve(ndisks=3):
    res = solve([list(range(ndisks - 1, -1, -1)), [], []], ndisks)
    final = []
    for p in res:
        final.append(p)
    assert final == [
        [[2, 1], [], [0]],
        [[2], [1], [0]],
        [[2], [1, 0], []],
        [[], [1, 0], [2]],
        [[0], [1], [2]],
        [[0], [], [2, 1]],
        [[], [], [2, 1, 0]],
    ]


def test_deepcopy_solve(ndisks=3):
    res = solve([list(range(ndisks - 1, -1, -1)), [], []], ndisks)
    final = []
    for p in res:
        final.append(copy.deepcopy(p))
    assert final == [
        [[2, 1], [], [0]],
        [[2], [1], [0]],
        [[2], [1, 0], []],
        [[], [1, 0], [2]],
        [[0], [1], [2]],
        [[0], [], [2, 1]],
        [[], [], [2, 1, 0]],
    ]
