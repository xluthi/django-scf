from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:competition_id>/', views.detail, name='detail'),
    path('<int:competition_id>/results/', views.results, name='results'),
    path('<int:competition_id>/<int:competitor_id>', views.athlete_results, name='athlete_results'),
    path('<int:competition_id>/encode/', views.encode, name='encode'),
    path('athlete/', views.athletes_index, name='athletes'),
    path('athlete/<int:athlete_id>/', views.athlete, name='athlete'),
]
