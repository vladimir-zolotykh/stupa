#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator

PegsT = tuple[list[int], list[int], list[int]]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    """Return a new peg configuration with a disk moved from one peg to another."""
    # Create deep copies of all pegs
    new_pegs = [peg[:] for peg in pegs]

    # Perform the move on the copies
    disk = new_pegs[from_].pop()
    new_pegs[to].append(disk)

    return new_pegs


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return

    # Make a working copy to avoid modifying the input
    current = [peg[:] for peg in pegs]

    # Recursively solve for n-1 disks from from_ to aux
    # This will yield all intermediate states
    yield from solve(current, ndisks - 1, from_, to, aux)

    # Move the largest disk from from_ to to
    current = move(current, from_, to)
    yield current

    # Recursively solve for n-1 disks from aux to to
    yield from solve(current, ndisks - 1, aux, from_, to)
