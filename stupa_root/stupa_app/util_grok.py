from typing import Generator

PegsT = tuple[list[int], list[int], list[int]]
# PegsT = list[list]


def move(pegs: PegsT, from_: int, to: int) -> PegsT:
    new_pegs = [list(peg) for peg in pegs]  # Fresh copy to avoid side effects
    disk = new_pegs[from_].pop()
    new_pegs[to].append(disk)
    return new_pegs


def solve(
    pegs: PegsT, ndisks: int, from_: int = 0, aux: int = 1, to: int = 2
) -> Generator[PegsT, None, PegsT]:
    if ndisks == 0:
        return pegs
    pegs = yield from solve(pegs, ndisks - 1, from_, to, aux)
    new_pegs = move(pegs, from_, to)
    yield new_pegs
    pegs = yield from solve(new_pegs, ndisks - 1, aux, from_, to)
    return pegs
