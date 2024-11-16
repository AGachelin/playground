from django.urls import path
from . import views


urlpatterns = [
    path("", views.view, name="view"),
    path('project/<str:pk>', views.character, name='detail'),
]
