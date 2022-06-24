from typing import List, Optional

from rest_framework.request import Request
from rest_framework.serializers import Serializer, ModelSerializer


class BaseSerializerMixin:

    def __init__(self: Serializer, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request: Optional[Request] = self.context.get('request')
        if request:
            fields: Optional[str] = request.query_params.get('fields')
            if fields:
                fields: List[str] = fields.split(',')
                allowed = set(fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)


class BaseModelSerializer(BaseSerializerMixin, ModelSerializer):
    pass
