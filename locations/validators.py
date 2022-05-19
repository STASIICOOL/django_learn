from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import requests


def validate_image_url(url):
    validate_url = URLValidator
    validate_url(url)
    if is_url_image(url):
        return url
    else:
        raise ValidationError(message="Error validation image")


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False