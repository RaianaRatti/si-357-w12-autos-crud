from django.urls import path

from . import views

app_name = "solo1"
urlpatterns = [
    path("", views.index, name="index"),
]
