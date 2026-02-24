#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import copy
import pytest

PegsT = tuple[list[int], list[int], list[int]]
# PegsT = list[list]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    # pegs = copy.deepcopy(pegs)
    src, dst = pegs[from_], pegs[to]
    disk = src.pop()
    dst.append(disk)
    return pegs


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


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return
    yield from solve(pegs, ndisks - 1, from_, to, aux)
    yield move(pegs, from_, to)
    # move(pegs, from_, to)
    # yield copy.deepcopy(pegs)

    yield from solve(pegs, ndisks - 1, aux, from_, to)


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
