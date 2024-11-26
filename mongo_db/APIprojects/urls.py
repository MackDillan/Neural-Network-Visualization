from django.urls import path
from .views import ProjectView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects'),
    path('projects/<str:pk>/', ProjectView.as_view(), name='project_detail'),
]
