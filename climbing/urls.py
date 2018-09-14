# (c) © 2018 Xavier Lüthi xavier@luthi.eu
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See LICENSE.txt for the full license text.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:competition_id>/', views.detail, name='detail'),
    path('<int:competition_id>/results/', views.results, name='results'),
    path('<int:competition_id>/<int:competitor_id>', views.athlete_results, name='athlete_results'),
    path('<int:competition_id>/encode/', views.encode, name='encode'),
    path('athletes/', views.athletes_index, name='athletes'),
    path('athlete/<int:athlete_id>/', views.athlete, name='athlete'),
]
