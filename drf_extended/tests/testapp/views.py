from rest_framework.generics import RetrieveAPIView

from .models import SomeModel


class SomeModelRetrieveAPIView(RetrieveAPIView):
    serializer_class = SomeModel.get_serializer_class()
    queryset = SomeModel.objects.select_related('parent').all()


get_some_model_view = SomeModelRetrieveAPIView.as_view()
