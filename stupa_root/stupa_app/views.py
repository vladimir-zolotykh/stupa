from django.shortcuts import render, redirect


def start(request):
    if request.method == "POST":
        n = int(request.POST.get("n", 3))
        delay = int(request.POST.get("delay", 500))

        if n < MIN_DISKS or n > MAX_DISKS:
            n = 3

        init_game(request, n, delay)
        return redirect("game")

    return render(request, "hanoi/start.html")


def game(request):
    if "pegs" not in request.session:
        return redirect("start")

    return render(
        request,
        "hanoi/game.html",
        {
            "pegs": request.session["pegs"],
            "delay": request.session["delay"],
        },
    )


def board(request):
    if "pegs" not in request.session:
        return redirect("start")

    return render(
        request,
        "hanoi/game.html",
        {
            "pegs": request.session["pegs"],
            "delay": request.session["delay"],
        },
    )
