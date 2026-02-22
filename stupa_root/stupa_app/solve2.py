#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import copy
import pytest

PegsT = tuple[list[int], list[int], list[int]]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    src, dst = pegs[from_], pegs[to]
    disk = src.pop()
    dst.append(disk)
    return pegs


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return
    yield from solve(pegs, ndisks - 1, from_, to, aux)
    yield move(pegs, from_, to)
    yield from solve(pegs, ndisks - 1, aux, from_, to)


# @pytest.mark.parametrize(
#     "ndisks, expected_nsteps",
#     [
#         (1, 1),
#         (2, 3),
#         (3, 7),
#         (4, 15),
#         (5, 31),
#         (6, 63),
#         (7, 127),
#         (8, 255),
#     ],
# )
def test_solve(ndisks, pegs):
    expected = copy.copy(pegs[0])
    result = solve(pegs, ndisks)
    print(f"{pegs = }, {expected = }")
    for r in result:
        print(r)
    assert result == expected


if __name__ == "__main__":
    pegs = [list(range(2, -1, -1)), [], []]
    test_solve(3, pegs)
