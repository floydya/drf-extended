from typing import Optional

import dataclasses

from rest_framework.serializers import Field


@dataclasses.dataclass
class APIField:
    name: str
    serializer: Optional[Field] = None

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<APIField {self.name}>"
