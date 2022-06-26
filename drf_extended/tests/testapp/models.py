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
    other_parents = models.ManyToManyField(ParentModel, related_name='+')

    api_fields = [
        APIField('name'),
        # APIField('description'),  – specially excluded for tests purposes.
        APIField('parent'),
        APIField(
            'parent_id',
            serializer=serializers.IntegerField(source='parent.id'),
        ),
        APIField('other_parents'),
    ]
