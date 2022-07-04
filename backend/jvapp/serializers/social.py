from jvapp.models import SocialPlatform


def get_serialized_social_platform(social_platform: SocialPlatform):
    return {
        'name': social_platform.name
    }
