from collections import UserDict
import copy


class Pegs(UserDict):
    def __init__(self, data: dict, step: int = 0):
        super().__init__(data)
        self.step = step

    @classmethod
    def from_ndisks(cls, ndisks):
        data = {
            "A": list(range(ndisks, 0, -1)),
            "B": [],
            "C": [],
        }
        return cls(data, 0)

    @classmethod
    def from_session(cls, request):
        return cls(request.session["pegs"], step=request.session["step"])

    def to_session(self, request):
        request.session["pegs"] = dict(copy.deepcopy(self.data))
        request.session["step"] = self.step

    def move(self, from_, to):
        src, dst = self.data[from_], self.data[to]
        if dst and src[-1] > dst[-1]:
            raise ValueError(f"Cannot place {src[-1]} on top {dst[-1]}")
        disk = src.pop()
        dst.append(disk)
        self.nsteps += 1

    def solve(self, ndisks: int, from_: str, aux: str, to: str):
        if ndisks == 0:
            return
        self.solve(ndisks - 1, from_, to, aux)
        self.move(from_, to)
        self.solve(ndisks - 1, aux, from_, to)


def solve(pegs: Pegs) -> int:
    pegs.solve(len(pegs["A"]), "A", "B", "C")
    return pegs.nsteps
