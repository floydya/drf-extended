from django.db import models

from drf_extended import APIMixin, APIModel, APIField
from rest_framework import serializers


class MyParentModel(APIMixin, models.Model):
    """
        You can inherit from APIMixin,
        that provides serializer constructor method.
    """
    name = models.CharField(max_length=64)
    description = models.TextField()

    api_fields = [
        APIField('name'),
        APIField('description'),
    ]


class MyModel(APIModel):
    """
        You can inherit from APIModel,
        that is inherited from APIMixin and models.Model.
    """
    title = models.CharField(max_length=40)
    parent = models.ForeignKey(MyParentModel, on_delete=models.CASCADE)

    api_fields = [
        # Plain serialize title as rest_framework does it out of the box.
        APIField('title'),
        # Serializer from foreign key field's model will be auto-calculated,
        # if ForeignKey related model is subclass of APIMixin(or APIModel).
        APIField('parent'),
        # You can specify custom serializer for field.
        APIField('parent_id', serializers.IntegerField(source='parent.id')),
    ]
