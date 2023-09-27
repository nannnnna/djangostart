from decimal import Decimal
import json
from django.core.serializers.json import DjangoJSONEncoder

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Преобразуем Decimal в строку
        return super(CustomJSONEncoder, self).default(obj)
