from django.urls import path

from .views import get_some_model_view


urlpatterns = [
    path('some-model/<int:pk>/', get_some_model_view),
]
