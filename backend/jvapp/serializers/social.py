from jvapp.models import SocialPlatform


def get_serialized_social_platform(social_platform: SocialPlatform):
    return {
        'id': social_platform.id,
        'name': social_platform.name,
        'logo': social_platform.logo.url if social_platform.logo else None
    }
