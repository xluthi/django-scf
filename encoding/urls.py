from django.urls import path

from . import views

app_name = 'encoding'
urlpatterns = [
    path('<int:competition_id>/', views.competition, name='competition'),
    path('<int:competition_id>/<int:competitor_id>', views.competitor, name='competitor'),
]
