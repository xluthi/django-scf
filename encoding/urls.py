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

app_name = 'encoding'
urlpatterns = [
    path('<int:competition_id>/', views.competition, name='competition'),
    path('<int:competition_id>/<int:competitor_id>', views.competitor, name='competitor'),
    path('<int:competition_id>/<int:competitor_id>/encode', views.encode, name='encode'),
    path('<int:competition_id>/boulder', views.list_boulders, name='list_boulders'),
    path('<int:competition_id>/boulder/<int:boulder_id>', views.boulder, name='boulder'),
    path('<int:competition_id>/boulder/<int:boulder_id>/encode', views.boulder_encode, name='boulder_encode'),
]
