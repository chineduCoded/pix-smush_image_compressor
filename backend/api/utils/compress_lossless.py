import base64
from io import BytesIO
from PIL import Image, ImageFilter


def compress_image(image_file):
    """
    Compresses an image using different compression algorithms based on the file format.

    Args:
        image_file (bytes): The image file to compress.

    Returns:
        bytes: The compressed image data as a bytes object. None if the image format is not supported.

    Raises:
        ValueError: If the image format is not supported (optional).
    """
    file_format = image_file.format
    size = image_file.size
    supported_formats = ['png', 'jpeg', 'jpg', 'webp']

    if file_format.lower() not in supported_formats:
        # Skip unsupported formats
        raise ValueError(f"{file_format} not supported!")

    resize_image = image_file.resize(
        size, resample=Image.LANCZOS, reducing_gap=2.0)

    # Compress the image based on the file format
    if file_format.lower() == 'png':
        saved_data = BytesIO()
        resize_image.save(saved_data, format='PNG', optimize=True)
    elif file_format.lower() in ['jpeg', 'jpg']:
        saved_data = BytesIO()
        resize_image.save(saved_data, format='JPEG',
                          quality=85, optimize=True, progressive=True)
    elif file_format.lower() == 'webp':
        saved_data = BytesIO()
        resize_image.save(saved_data, format='WEBP',
                          lossless=True, method=5, quality=90, exact=True)
    else:
        saved_data = None

    if saved_data is not None:
        saved_data.seek(0)  # Reset the file pointer to the beginning
        return saved_data.getvalue()

    return None
