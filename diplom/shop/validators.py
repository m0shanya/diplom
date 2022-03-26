from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

MAX_UPLOAD_PHOTO_WIDTH_SMALL = 450
MAX_UPLOAD_PHOTO_HEIGHT_SMALL = 300
MAX_UPLOAD_PHOTO_WIDTH_BIG = 600
MAX_UPLOAD_PHOTO_HEIGHT_BIG = 700
MAX_UPLOAD_PHOTO_WIDTH_CART = 80
MAX_UPLOAD_PHOTO_HEIGHT_CART = 80


def image_resolution_check_small(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width != MAX_UPLOAD_PHOTO_WIDTH_SMALL or image_height != MAX_UPLOAD_PHOTO_HEIGHT_SMALL:
        raise ValidationError(f'Image resolution must be {MAX_UPLOAD_PHOTO_WIDTH_SMALL}x{MAX_UPLOAD_PHOTO_HEIGHT_SMALL}')


def image_resolution_check_big(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width > MAX_UPLOAD_PHOTO_WIDTH_BIG or image_height > MAX_UPLOAD_PHOTO_HEIGHT_BIG:
        raise ValidationError(f'Image resolution must be {MAX_UPLOAD_PHOTO_WIDTH_BIG}x{MAX_UPLOAD_PHOTO_HEIGHT_BIG}')


def image_resolution_check_cart(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width != MAX_UPLOAD_PHOTO_WIDTH_CART or image_height != MAX_UPLOAD_PHOTO_HEIGHT_CART:
        raise ValidationError(f'Image resolution must be {MAX_UPLOAD_PHOTO_WIDTH_CART}x{MAX_UPLOAD_PHOTO_HEIGHT_CART}')
