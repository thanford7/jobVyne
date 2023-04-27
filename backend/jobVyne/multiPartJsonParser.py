from django.conf import settings
from django.http import QueryDict
import json
from rest_framework import parsers
from rest_framework.parsers import FormParser


class MultiPartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        # find the data field and parse it
        data = json.loads(result.data['data'])
        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)
    
    
class RawFormParser(FormParser):
    
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        data = stream.read()
        qdict = QueryDict(data, encoding=encoding, mutable=True)
        qdict.update(_raw_data=data.decode(encoding))
        return qdict
