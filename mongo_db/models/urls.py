from django.urls import path
from .views import ModelsView, JSONDataDownloadView

urlpatterns = [
    path('models/', ModelsView.as_view(), name='models'),
    path('models/<str:pk>/', ModelsView.as_view(), name='model-detail'),
    path('models/d/<str:pk>/', JSONDataDownloadView.as_view(), name='json-data-download'),
    
]
