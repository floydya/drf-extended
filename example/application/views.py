from rest_framework.generics import RetrieveAPIView

from application.models import MyModel


class MyModelDetailAPIView(RetrieveAPIView):
    serializer_class = MyModel.get_serializer_class()
    queryset = MyModel.objects.select_related('parent').all()
