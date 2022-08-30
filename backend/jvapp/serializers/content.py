from jvapp.models.content import *
from jvapp.utils.datetime import get_datetime_format_or_none


def get_serialized_content_item(content_item: ContentItem):
    return {
        'id': content_item.id,
        'header': content_item.header,
        'type': content_item.type,
        'config': content_item.config,
        'item_parts': content_item.item_parts
    }


def get_serialized_social_post(social_post: SocialPost):
    return {
        'id': social_post.id,
        'user_id': social_post.user_id,
        'employer_id': social_post.employer_id,
        'content': social_post.content,
        'formatted_content': social_post.formatted_content,
        'files': [{'id': f.id, 'url': f.file.url, 'title': f.file.name} for f in social_post.file.all()],
        'posts': [{
            'email': a.email, 'platform': a.platform, 'posted_dt': get_datetime_format_or_none(a.posted_dt)
        } for a in social_post.audit.all()],
        'created_dt': get_datetime_format_or_none(social_post.created_dt)
    }
