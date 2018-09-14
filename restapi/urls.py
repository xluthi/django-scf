from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('results/', views.result_list),
    path('results/<int:pk>/', views.result_detail),
    path('competitors/', views.CompetitorList.as_view()),
    path('competitors/<int:pk>', views.CompetitorDetail.as_view()),
    path('athletes/', views.AthleteList.as_view()),
    path('athletes/<int:pk>', views.AthleteDetail.as_view(), name="athlete-detail"),
    path('clubs/', views.ClubList.as_view()),
    path('clubs/<int:pk>', views.ClubDetail.as_view(), name="club-detail"),
]


urlpatterns = format_suffix_patterns(urlpatterns)
