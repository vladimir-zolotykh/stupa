from django.urls import path
from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path("game/", views.GameView.as_view(), name="game"),
    path("board/", views.board, name="board"),
]
