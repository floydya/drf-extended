from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

try:
    from django.contrib.gis.geos import Point, GEOSException  # pylint: disable=ungrouped-imports
except (ImproperlyConfigured, ImportError):
    LocationField = serializers.Field
else:
    from django.utils.translation import gettext_lazy as _

    USE_DRF_YASG = False
    try:
        from drf_yasg import openapi
        USE_DRF_YASG = True
    except ImportError:
        pass

    class LocationField(serializers.Field):
        default_error_messages = {'invalid': _('Enter a valid location.')}

        class Meta:
            if USE_DRF_YASG:
                swagger_schema_fields = {
                    'type': openapi.TYPE_OBJECT,
                    'title': 'Location',
                    'properties': {
                        'lng': openapi.Schema(
                            title='Longitude',
                            type=openapi.TYPE_NUMBER,
                        ),
                        'lat': openapi.Schema(
                            title='Latitude',
                            type=openapi.TYPE_NUMBER,
                        ),
                    },
                    'required': ['lng', 'lat'],
                 }

        def to_internal_value(self, data):  # pylint: disable=inconsistent-return-statements
            if data in (None, '', [], (), {}):
                return None

            if data and isinstance(data, dict):
                try:
                    lng = data.get('lng')
                    lat = data.get('lat')
                    return Point(lng, lat)
                except (GEOSException, TypeError, ValueError):
                    self.fail('invalid')
            self.fail('invalid')

        def to_representation(self, value):
            if value is None:
                return None
            return {'lng': value.x, 'lat': value.y}
