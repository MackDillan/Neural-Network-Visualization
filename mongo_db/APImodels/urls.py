from django.urls import path
from .views import ModelsView, ModelDownloadView

urlpatterns = [
    path('models/', ModelsView.as_view(), name='models'),
    path('models/<str:pk>/', ModelsView.as_view(), name='model-detail'),
    path('models/d/<str:pk>/', ModelDownloadView.as_view(), name='json-data-download'),
    
]
