from django.urls import path
from . import views

app_name = "sc"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_event, name="add_event"),
    path("list/", views.get_events, name="get_events"),
    path("remove/", views.remove_event, name="remove_event"),
    path("move/", views.drop_event, name="drop_event"),
    path("resize/", views.resize_event, name="resize_event"),
]
