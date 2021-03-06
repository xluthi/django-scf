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

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='climbing/', permanent=True)),
    path('climbing/', include('climbing.urls')),
    path('v2/',       include('frontendjs.urls')),
    path('encoding/', include('encoding.urls')),
    path('rest/',     include('restapi.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
