from django.urls import path

from . import views

app_name = 'encoding'
urlpatterns = [
    path('<int:competition_id>/', views.competition, name='competition'),
    path('<int:competition_id>/<int:competitor_id>', views.competitor, name='competitor'),
    path('<int:competition_id>/<int:competitor_id>/encode', views.encode, name='encode'),
    path('<int:competition_id>/boulder', views.list_boulders, name='list_boulders'),
    path('<int:competition_id>/boulder/<int:boulder_id>', views.boulder, name='boulder'),
    path('<int:competition_id>/boulder/<int:boulder_id>/encode', views.boulder_encode, name='boulder_encode'),
]
