#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator

PegsT = tuple[list[int], list[int], list[int]]
# PegsT = list[list]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    # Non-destructive move: returns a new tuple of lists
    new_pegs = list(list(p) for p in pegs)  # Deep copy the outer structure
    disk = new_pegs[from_].pop()
    new_pegs[to].append(disk)
    return tuple(new_pegs)


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return

    # 1. Solve the sub-problem (n-1 disks)
    current_state = pegs
    for state in solve(current_state, ndisks - 1, from_, to, aux):
        yield state
        current_state = state  # Track the last produced state

    # 2. Move the largest disk from the LAST state produced
    current_state = move(current_state, from_, to)
    yield current_state

    # 3. Solve the remaining sub-problem starting from the NEW state
    yield from solve(current_state, ndisks - 1, aux, from_, to)
