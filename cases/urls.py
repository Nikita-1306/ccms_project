from django.urls import path
from . import views
urlpatterns = [
    path('cases/<int:pk>/download/', views.download_report, name='download_report'),
    path('', views.home, name='home'),
    path('cases/new/', views.case_create, name='case_create'),
    path('cases/my/', views.my_cases, name='my_cases'),
    path('cases/<int:pk>/', views.case_detail, name='case_detail'),
    path('cases/<int:pk>/edit/', views.case_edit, name='case_edit'),
    path('cases/<int:pk>/delete/', views.case_delete, name='case_delete'),
    path('cases/track/', views.track_case, name='track_case'),
]
