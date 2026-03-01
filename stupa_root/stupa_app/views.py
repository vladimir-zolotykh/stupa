from django.views import View
from django.shortcuts import render, redirect
import logging
from . import solve
from . import solve2


logger = logging.getLogger(__name__)


class StartView(View):
    template_name = "stupa_app/start.html"

    def post(self, request):
        ndisks = int(request.POST.get("ndisks", 3))
        delay = int(request.POST.get("delay", 500))
        self.init_game(request, ndisks, delay)
        return redirect("game")

    def get(self, request):
        return render(request, self.template_name)

    def init_game(self, request, ndisks, delay):
        pegs_start = [list(range(ndisks - 1, -1, -1)), [], []]
        pegs = [pegs_start, *list(solve2.solve(pegs_start, ndisks))]
        request.session["pegs"] = pegs
        request.session["ndisks"] = ndisks
        request.session.modified = True


class GameView(View):
    template_name = "stupa_app/game.html"

    def post(self, request):
        action = request.POST.get("action")
        if action == "next":
            pegs = request.session.get("pegs")
            pegs_car, *pegs_rest = pegs
            request.session["pegs"] = pegs_rest
            return redirect("game")
        if action == "restart":
            return redirect("start")

    def get(self, request):
        pegs = request.session.get("pegs")
        ndisks = request.session.get("ndisks")
        solved = self.is_solved(pegs[0], ndisks)
        logger.debug("pegs: %s", pegs)
        # transposed = solve.transpose(solve2.inflate(pegs[0], ndisks))
        transposed = solve2.inflate(pegs[0], ndisks)
        logger.debug("transposed: %s", transposed)

        disk_classes = {disk: f"disk disk-{disk}" for disk in range(ndisks)}
        return render(
            request,
            self.template_name,
            context={
                "pegs": transposed,
                "ndisks": ndisks,
                "solved": solved,
                "disk_styles": self.get_disk_styles(ndisks),
                "disk_classes": disk_classes,
            },
        )

    def get_disk_styles(self, ndisks: int) -> dict:
        disk_styles = {}

        min_width = 30
        max_width = 100
        step = (max_width - min_width) / (ndisks - 1)
        hue_step = 360 / ndisks

        for disk in range(ndisks):
            width = min_width + disk * step
            hue = disk * hue_step

            disk_styles[disk] = {
                "width": round(width, 2),
                "hue": round(hue, 2),
            }
        return disk_styles

    def is_solved(self, pegs, ndisks):
        return pegs == [[], [], list(range(ndisks - 1, -1, -1))]


def board(request):
    return render(request, "stupa_app/board.html")
