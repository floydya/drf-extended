from unittest import TestCase
from urllib.parse import urlencode

from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .testapp.models import ParentModel, SomeModel
from .testapp.views import get_some_model_view
from .. import APIField
from ..serializers import BaseModelSerializer


class TestPackage:

    def setup(self):
        self.p_model = ParentModel(
            id=1, title="Test title", description="Desc"
        )
        self.p_model.save()
        self.model = SomeModel(
            name="Name", parent=self.p_model, description="test"
        )
        self.model.save()

    def test_serializer_class(self):
        p_serializer = self.p_model.get_serializer_class()
        assert issubclass(p_serializer, BaseModelSerializer)
        assert issubclass(p_serializer, Serializer)
        assert 'title' in p_serializer().get_fields()
        assert 'description' in p_serializer().get_fields()

        serializer = self.model.get_serializer_class()
        assert issubclass(serializer, BaseModelSerializer)
        assert 'parent' in serializer().get_fields()
        nested_parent_serializer = serializer().get_fields()['parent']
        assert issubclass(nested_parent_serializer.__class__, BaseModelSerializer)

    def test_serializer_data(self):
        p_serializer = self.p_model.get_serializer_class()
        parent_data = p_serializer(self.p_model).data
        TestCase().assertDictEqual(parent_data, {
            'title': self.p_model.title,
            'description': self.p_model.description,
        })

    def test_nested_serializer_data(self):
        serializer = self.model.get_serializer_class()
        data = serializer(self.model).data
        TestCase().assertDictEqual(
            data.get('parent'), {
                'title': self.p_model.title,
                'description': self.p_model.description
            }
        )

    def test_api_field(self):
        api_field = APIField(name='test')
        assert api_field.serializer is None
        assert api_field.name == 'test'
        assert hasattr(api_field, '__hash__')
        assert hash('test') == hash(api_field)
        assert repr(api_field) == '<APIField test>'

    def test_graphql_query_params(self):
        query_params = {'fields': 'name,parent_id'}
        qs = urlencode(query_params)
        request = RequestFactory().get(f'/some-model/{self.model.pk}/?{qs}')
        response: Response = get_some_model_view(request, pk=self.model.pk)
        TestCase().assertDictEqual(response.data, {
            'name': self.model.name,
            'parent_id': self.p_model.pk
        })
