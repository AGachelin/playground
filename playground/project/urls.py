from django.urls import path
from . import views


urlpatterns = [
    path("", views.view, name="view"),
    path("project/<str:pk>", views.detail, name="detail"),
    path("project/<str:pk>/?<str:message>", views.detail, name="character_detail_mes"),
]
