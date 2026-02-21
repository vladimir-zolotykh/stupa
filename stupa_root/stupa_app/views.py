from django.shortcuts import render, redirect
import logging
from . import solve


logger = logging.getLogger(__name__)


def init_game(request, ndisks, delay):
    pegs = solve.Pegs.from_ndisks(ndisks)
    request.session["pegs"] = pegs.to_session_dict()
    request.session.modified = True


def start(request):
    if request.method == "POST":
        ndisks = int(request.POST.get("ndisks", 3))
        delay = int(request.POST.get("delay", 500))
        init_game(request, ndisks, delay)
        return redirect("game")

    return render(request, "stupa_app/start.html")


def game(request):
    if request.method == "POST":
        return redirect("game")
    pegs = request.session.get("pegs")
    pegs = solve.Pegs.from_session_dict(pegs) if pegs else solve.Pegs.from_ndisks()
    logger.debug("Pegs object: %s", pegs)
    logger.debug("Pegs data: %s", pegs.data)
    return render(
        request,
        "stupa_app/game.html",
        context={
            # "pegs_data": pegs.data,
            "pegs_data": solve.transpose(list(pegs.data.values())),
            "ndisks": pegs.ndisks,
            "step": pegs.step,
        },
    )


def board(request):
    return render(request, "stupa_app/board.html")
