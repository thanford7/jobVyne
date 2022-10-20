import magic

from jvapp.models.abstract import ALLOWED_UPLOADS_IMAGE, ALLOWED_UPLOADS_VIDEO


def get_file_extension(file_url):
    return file_url.split('.')[-1]


def get_file_name(file_url):
    return file_url.split('/')[-1]


def get_mime_from_file_path(file_path):
    mime = magic.from_file(file_path, mime=True)
    return mime


def get_mime_from_in_memory_file(in_memory_file):
    mime = magic.from_buffer(in_memory_file.read(), mime=True)
    return mime


def is_image_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_IMAGE


def is_video_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_VIDEO
