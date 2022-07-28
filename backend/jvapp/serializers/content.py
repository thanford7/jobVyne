from jvapp.models.content import *


def get_serialized_content_item(content_item: ContentItem):
    return {
        'id': content_item.id,
        'header': content_item.header,
        'type': content_item.type,
        'config': content_item.config,
        'item_parts': content_item.item_parts
    }
