from django.shortcuts import render, redirect
import logging
from . import solve
from . import solve2


logger = logging.getLogger(__name__)


def init_game(request, ndisks, delay):
    pegs_start = [list(range(ndisks - 1, -1, -1)), [], []]
    pegs = [pegs_start, *list(solve2.solve(pegs_start, ndisks))]
    request.session["pegs"] = pegs
    request.session["ndisks"] = ndisks
    request.session.modified = True


def start(request):
    if request.method == "POST":
        ndisks = int(request.POST.get("ndisks", 3))
        delay = int(request.POST.get("delay", 500))
        init_game(request, ndisks, delay)
        return redirect("game")

    return render(request, "stupa_app/start.html")


def is_solved(pegs, ndisks):
    return pegs == [[], [], list(range(ndisks - 1, -1, -1))]


def game(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "next":
            pegs = request.session.get("pegs")
            pegs_car, *pegs_rest = pegs
            request.session["pegs"] = pegs_rest
            return redirect("game")
        if action == "restart":
            return redirect("start")
    pegs = request.session.get("pegs")
    ndisks = request.session.get("ndisks")
    solved = is_solved(pegs[0], ndisks)
    logger.debug("pegs: %s", pegs)
    transposed = pegs
    transposed = solve.transpose(solve2.inflate(pegs[0], ndisks))
    logger.debug("transposed: %s", transposed)
    return render(
        request,
        "stupa_app/game.html",
        context={
            "pegs": transposed,
            "ndisks": ndisks,
            "solved": solved,
        },
    )


def board(request):
    return render(request, "stupa_app/board.html")
