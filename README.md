![lint](https://github.com/floydya/drf-extended/actions/workflows/lint.yml/badge.svg)
![deploy](https://github.com/floydya/drf-extended/actions/workflows/deploy.yml/badge.svg)
![pypi](https://badge.fury.io/py/drf-extended.svg)

# DRF extended  

This package provides ability for developers to create serializers directly from models.  

## Installation  

### Supported:
* Python 3.7+
* Django 3.0+
* DRF 3+

### Install using pip:  

```bash  
pip install drf-extended
```  

## Usage  

### Models file:

```python  
from django.db import models

from drf_extended import APIMixin, APIModel, APIField
from rest_framework import serializers

class MyParentModel(APIMixin, models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    api_fields = [
        APIField('name'),
        APIField('description'),
    ]

class MyModel(APIMixin, models.Model):
    title = models.CharField(max_length=40)
    parent = models.ForeignKey(MyParentModel, on_delete=models.CASCADE)
  
    api_fields = [
        # Plain serialize title as rest_framework does it out of the box.
        APIField('title'),
        # Serializer from foreign key field's model will be calculated automatically,
        # if ForeingKey related model is subclass of APIMixin.
        APIField('parent'),
        # You can specify custom serializer for field.
        APIField('parent_id', serializers.IntegerField(source='parent.id')),
    ]
```

### Get serializer:

```python
from .models import MyModel

MyModelSerializer = MyModel.get_serializer_class()
```
#### Here, MyModelSerializer is equal to:
```python
from rest_framework import serializers
from .models import MyParentModel


class MyParentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyParentModel
        fields = ('name', 'description')

class MyModelSerializer(serializers.ModelSerializer):
    parent = MyParentModelSerializer()

    class Meta:
        fields = ('title', 'parent', 'parent_id')

```

### Use in views:
```python

from rest_framework.generics import RetrieveAPIView

from .models import MyModel


class MyModelRetrieveView(RetrieveAPIView):
    serializer_class = MyModel.get_serializer_class()
    queryset = MyModel.objects.select_related('parent').all()

```

#### Using such serializer in views allows us to get only those fields that we specify in the request query params with key `fields`.
E.g. `GET /some-model/<pk>/?fields=id,parent_id`, results us:
```json
{
    "id": <pk>,
    "parent_id": <pk>
}
```
