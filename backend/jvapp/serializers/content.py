from jvapp.models.content import *
from jvapp.serializers.social import get_serialized_social_platform
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
        'user_name': f'{social_post.user.first_name} {social_post.user.last_name}' if social_post.user else None,
        'employer_id': social_post.employer_id,
        'content': social_post.content,
        'formatted_content': social_post.formatted_content,
        'platform': get_serialized_social_platform(social_post.social_platform),
        'files': [{'id': f.id, 'url': f.file.url, 'title': f.file.name} for f in social_post.file.all()],
        'posts': [{
            'email': a.email, 'platform': a.platform, 'posted_dt': get_datetime_format_or_none(a.posted_dt)
        } for a in social_post.audit.all()],
        'child_posts_count': social_post.child_post.count(),
        'created_dt': get_datetime_format_or_none(social_post.created_dt),
        'is_auto_post': social_post.is_auto_post,
        'auto_start_dt': get_datetime_format_or_none(social_post.auto_start_dt),
        'auto_weeks_between': social_post.auto_weeks_between,
        'auto_day_of_week': social_post.auto_day_of_week,
        'post_account_ids': [pc.id for pc in social_post.post_credentials.all()],
        'link_filter_id': social_post.link_filter_id
    }
