from django.shortcuts import render, redirect
import logging
from . import solve
from . import solve2


logger = logging.getLogger(__name__)


def init_game(request, ndisks, delay):
    pegs_start = [list(range(ndisks - 1, -1, -1)), [], []]
    # pegs = pegs_start.extend(list(solve2.solve(pegs_start, ndisks)))
    pegs = [pegs_start, *list(solve2.solve(pegs_start, ndisks))]
    request.session["pegs"] = pegs
    request.session["ndisks"] = ndisks
    # pegs = solve.Pegs.from_ndisks(ndisks)
    # request.session["pegs"] = pegs.to_session_dict()
    request.session.modified = True


def start(request):
    if request.method == "POST":
        ndisks = int(request.POST.get("ndisks", 3))
        delay = int(request.POST.get("delay", 500))
        init_game(request, ndisks, delay)
        return redirect("game")

    return render(request, "stupa_app/start.html")


def is_solved(pegs):
    return not pegs[0] and not pegs[1]


def game(request):
    if request.method == "POST":
        pegs = request.session.get("pegs")
        pegs_car, *pegs_rest = pegs
        request.session["pegs"] = pegs_rest
        return redirect("game")
    pegs = request.session.get("pegs")
    ndisks = request.session.get("ndisks")
    # pegs = solve.Pegs.from_session_dict(pegs) if pegs else solve.Pegs.from_ndisks()
    logger.debug("pegs: %s", pegs)
    # logger.debug("pegs_car: %s", pegs_car)
    # if not is_solved(pegs):
    # transposed = solve.inflate(solve.transpose(pegs[0]), ndisks)
    # transposed = solve.transpose(pegs[0])
    transposed = solve.transpose(solve2.inflate(pegs[0], ndisks))
    logger.debug("transposed: %s", transposed)
    return render(
        request,
        "stupa_app/game.html",
        context={
            # "pegs_data": pegs.data,
            # "pegs_data": solve.transpose(list(pegs.data.values())),
            "pegs": transposed,
            "ndisks": ndisks,
            "solved": is_solved(pegs),
        },
    )


def board(request):
    return render(request, "stupa_app/board.html")
