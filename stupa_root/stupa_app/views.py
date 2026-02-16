from django.shortcuts import render, redirect


def start(request):
    return render(request, "stupa_app/start.html")


def game(request):
    return render(request, "stupa_app/game.html")


def board(request):
    return render(request, "stupa_app/board.html")
