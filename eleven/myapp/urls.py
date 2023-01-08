from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name="index"),
    path('team/',views.teams,name='team'),
    path('team/finalteam/',views.finalteam,name='finalteam')
]