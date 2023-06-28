from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import requests
from PIL import Image
from django.core.files import File

from jvapp.utils.file import get_file_extension


def resize_image_with_fill(image, width, height):
    '''
    Resize PIL image keeping ratio and using transparent background.
    '''
    try:
        image.open()
        im = Image.open(image)
    except FileNotFoundError:
        return None
    ratio_w = width / im.width
    ratio_h = height / im.height
    if ratio_w < ratio_h:
        # Fixed by width
        resize_width = width
        resize_height = round(ratio_w * im.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * im.width)
        resize_height = height
    image_resize = im.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    if get_file_extension(image.url) != 'png':
        background = background.convert(mode='RGB')
    im.close()
    image.close()
    background_file = NamedTemporaryFile()
    try:
        background.save(background_file, format=get_file_extension(image.url))
    except KeyError:
        background.save(background_file, format='png')
    return background_file


def convert_url_to_image(image_url, file_name, is_use_request=False):
    if not image_url:
        return None
    image = NamedTemporaryFile()
    if is_use_request:
        # Sometimes urlopen gets a Forbidden error so we need to use a request
        image_data = requests.get(image_url).content
    else:
        image_data = urlopen(image_url).read()
    image.write(image_data)
    image.flush()
    return File(image, name=file_name)
