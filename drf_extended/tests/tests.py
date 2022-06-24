from django.db import models

from .testapp.models import ParentModel, SomeModel
from ..serializers import BaseModelSerializer


class TestPackage:

    def setup(self):
        self.p_model = ParentModel(
            id=1, title="Test title", description="Desc"
        )
        self.model = SomeModel(
            name="Name", parent=self.p_model, description="test"
        )

    def test_serializer(self):
        p_serializer = self.p_model.get_serializer_class()
        assert issubclass(p_serializer, BaseModelSerializer)

