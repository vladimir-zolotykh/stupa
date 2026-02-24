#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import copy
import pytest

PegsT = tuple[list[int], list[int], list[int]]
# PegsT = list[list]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    # Make a fresh copy of the pegs (no mutation)
    new_pegs = [list(p) for p in pegs]
    if not new_pegs[from_]:
        raise ValueError(f"Cannot move from empty peg {from_}")
    disk = new_pegs[from_][-1]
    new_pegs[from_] = new_pegs[from_][:-1]
    new_pegs[to] = new_pegs[to] + [disk]
    return tuple(new_pegs)


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return
    # recurse on smaller problem
    yield from solve(pegs, ndisks - 1, from_, to, aux)

    # update pegs with the move
    pegs = move(pegs, from_, to)
    yield pegs

    # recurse again with updated state
    yield from solve(pegs, ndisks - 1, aux, from_, to)
