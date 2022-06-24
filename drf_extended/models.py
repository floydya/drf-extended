from typing import Type, List, Dict, Union, Literal

from django.db import models
from django.db.models import ManyToManyField, ForeignKey
from rest_framework.serializers import Serializer

from .serializers import BaseSerializerMixin, BaseModelSerializer
from .types import APIField


class APIMixin:
    api_fields: List[APIField] = []

    @classmethod
    def get_serializer_class(
            cls: Type['APIMixin']
    ) -> Type[BaseSerializerMixin]:
        """Generate serializer based on model class."""
        api_fields: List[APIField] = cls.api_fields
        child_serializers: Dict[str, Type[Serializer]] = {}
        for field in cls._meta.get_fields():
            if field.is_relation and getattr(field, 'related_model'):
                properties = {}
                if isinstance(field, ManyToManyField):
                    properties = {'many': True}
                elif isinstance(field, ForeignKey):
                    pass
                else:
                    continue
                related_serializer = field.related_model.get_serializer_class()
                child_serializers[field.name] = related_serializer(
                    **properties
                )

        meta_fields: Union[Literal['__all__'], List[str]] = [
            api_field.name for api_field in api_fields
        ] or '__all__'

        child_serializers.update({
            api_field.name: api_field.serializer
            for api_field in api_fields
            if api_field.serializer
        })

        serializer_name = f'{cls.__name__}Serializer'

        class Meta:
            """Create Meta class with provided model and calculated fields."""
            model = cls
            fields = meta_fields

        return type(serializer_name, (BaseModelSerializer,), {
            **child_serializers,
            'Meta': Meta
        })


class APIModel(APIMixin, models.Model):

    class Meta:
        abstract = True
