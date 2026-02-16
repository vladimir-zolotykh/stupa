from django.urls import path, include

urlpatterns = [
    path("", include("stupa_app.urls")),
]
