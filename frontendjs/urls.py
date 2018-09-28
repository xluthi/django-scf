from django.urls import path
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('',  RedirectView.as_view(url='competitions/', permanent=True)),
    path('competitions/', TemplateView.as_view(template_name="frontendjs/competitions.html"), name="competitions"),
    path('competitions/<int:id>', TemplateView.as_view(template_name="frontendjs/competitions.html")),
]
