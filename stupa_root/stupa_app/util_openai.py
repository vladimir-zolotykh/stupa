from typing import Iterator
import copy

PegsT = tuple[list[int], list[int], list[int]]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    new_pegs = copy.deepcopy(pegs)  # Create a deep copy
    src, dst = new_pegs[from_], new_pegs[to]
    disk = src.pop()
    dst.append(disk)
    return new_pegs


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Iterator[PegsT]:
    if ndisks == 0:
        return
    yield from solve(pegs, ndisks - 1, from_, to, aux)
    yield move(pegs, from_, to)  # Use the modified move function
    yield from solve(pegs, ndisks - 1, aux, from_, to)
