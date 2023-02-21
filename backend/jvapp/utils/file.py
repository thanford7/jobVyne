import mimetypes

from jvapp.models.abstract import ALLOWED_UPLOADS_IMAGE, ALLOWED_UPLOADS_VIDEO


def get_file_extension(file_url):
    return file_url.split('.')[-1]


def get_file_name(file_url):
    return file_url.split('/')[-1]


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
