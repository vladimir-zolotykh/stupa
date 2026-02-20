from typing import Self
from collections import UserDict


class Pegs(UserDict):
    def __init__(self, data: dict, ndisks: int = 3, step: int = 0):
        super().__init__(data)
        self.step: int = step
        self.ndisks: int = ndisks

    def to_session_dict(self) -> dict:
        return {
            "data": dict(self.data),
            "ndisks": self.ndisks,
            "step": self.step,
        }

    @classmethod
    def from_ndisks(cls, ndisks: int = 3) -> Self:
        data = {"A": list(range(ndisks, 0, -1)), "B": [], "C": []}
        return cls(data, ndisks=ndisks, step=0)

    @classmethod
    def from_session_dict(cls, data: dict) -> Self:
        if not data:
            return cls.from_ndisks()
        return cls(
            data=data["data"],
            ndisks=data["ndisks"],
            step=data["step"],
        )

    def move(self, from_, to):
        src, dst = self.data[from_], self.data[to]
        if dst and src[-1] > dst[-1]:
            raise ValueError(f"Cannot place {src[-1]} on top {dst[-1]}")
        disk = src.pop()
        dst.append(disk)
        self.step += 1

    def solve(self, ndisks: int, from_: str, aux: str, to: str):
        if ndisks == 0:
            return
        self.solve(ndisks - 1, from_, to, aux)
        self.move(from_, to)
        self.solve(ndisks - 1, aux, from_, to)


def solve(pegs: Pegs) -> int:
    pegs.solve(len(pegs["A"]), "A", "B", "C")
    return pegs.step


def transpose(pegs: list[list]) -> list[list]:
    board = []
    npegs = len(pegs)  # number of pegs
    ndisks = len(pegs[0])  # number of disks
    for i in range(ndisks - 1, -1, -1):
        row = []
        for j in range(npegs):
            try:
                row.append(pegs[j][i])
            except IndexError:
                row.append(None)
        board.append(row)
    return board
