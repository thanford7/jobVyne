from jvapp.models.abstract import ALLOWED_UPLOADS_IMAGE, ALLOWED_UPLOADS_VIDEO


def get_file_extension(file_url):
    return file_url.split('.')[-1]


def is_image_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_IMAGE


def is_video_file(file_url):
    extension = get_file_extension(file_url)
    return extension in ALLOWED_UPLOADS_VIDEO
