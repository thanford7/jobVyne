import mimetypes

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from jobVyne.customStorage import OverwriteStorage
from jvapp.models.abstract import ALLOWED_UPLOADS_IMAGE, ALLOWED_UPLOADS_VIDEO


def get_user_upload_location(instance, filename):
    if hasattr(instance, 'user_id') and instance.user:
        email = instance.user.email
    else:
        email = instance.email
    
    return f'user/{email}/{filename}'


def get_file_storage_engine():
    return OverwriteStorage() if settings.IS_LOCAL else S3Boto3Storage()


def get_file_extension(file_url):
    if '.' not in file_url:
        return 'png'
    file_extension = file_url.split('.')[-1]
    file_extension = file_extension.split('?')[0]
    return file_extension


def get_file_name(file_url, is_include_extension=True):
    file_name = file_url.split('/')[-1]
    if is_include_extension:
        return file_name
    return file_name.split('.')[0]


def get_safe_file_path(file):
    # S3 file storage doesn't support an absolute path so we fall back to the URL location of the file
    try:
        return file.path
    except NotImplementedError:
        # return file.name
        return file.url


def get_mime_from_file_path(file_path):
    return mimetypes.guess_type(file_path)


def is_image_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_IMAGE


def is_video_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_VIDEO
