import json

from jvapp.models.content import *


def get_serialized_content_item(content_item: ContentItem):
    return {
        'id': content_item.id,
        'header': content_item.header,
        'type': content_item.type,
        'item_parts': json.dumps(content_item.item_parts)
    }
