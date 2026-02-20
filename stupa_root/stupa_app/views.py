from django.shortcuts import render, redirect
from . import solve


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
    pegs = request.session.get("pegs")
    pegs = solve.Pegs.from_session_dict(pegs) if pegs else solve.Pegs.from_ndisks()
    return render(
        request,
        "stupa_app/game.html",
        context={
            "pegs_data": solve.transpose(pegs.data),
            "ndisks": pegs.ndisks,
            "step": pegs.step,
        },
    )


def board(request):
    return render(request, "stupa_app/board.html")
