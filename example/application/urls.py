from django.urls import path

from application.views import MyModelDetailAPIView

urlpatterns = [
    path('my-model/', MyModelDetailAPIView.as_view()),
]
