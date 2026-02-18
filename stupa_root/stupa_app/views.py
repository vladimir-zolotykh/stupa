from django.shortcuts import render, redirect
from . import solve


def init_game(request, ndisks, delay):
    request.session["ndisks"] = ndisks
    request.session["delay"] = delay
    request.session["pegs"] = solve.Pegs(ndisks).to_session()


def start(request):
    if request.method == "POST":
        ndisks = int(request.POST.get("ndisks", 3))
        delay = int(request.POST.get("delay", 500))
        init_game(request, ndisks, delay)
        return redirect("game")

    return render(request, "stupa_app/start.html")


def game(request):
    pegs = solve.from_session(request)
    return render(request, "stupa_app/game.html", context={"pegs": pegs})


def board(request):
    return render(request, "stupa_app/board.html")
