from django.db import models
from rest_framework import serializers

from drf_extended import APIMixin, APIField


class ParentModel(APIMixin, models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    api_fields = [
        APIField('title'),
        APIField('description'),
    ]


class SomeModel(APIMixin, models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)

    api_fields = [
        APIField('name'),
        APIField('parent'),
        APIField(
            'parent_id',
            serializer=serializers.IntegerField(source='parent.id'),
        ),
    ]
