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


def decompress_image(compressed_data, original_format):
    """
    Decompresses a compressed image data and returns the uncompressed image.

    Args:
        compressed_data (bytes): The compressed image data as a bytes object.
        original_format (str): The original format of the image ('png', 'jpeg', 'jpg', 'webp').

    Returns:
        PIL.Image.Image: The decompressed image as a PIL Image object.

    Raises:
        ValueError: If the original format is not supported.
        IOError: If there is an error decompressing the image.
    """
    supported_formats = ['png', 'jpeg', 'jpg', 'webp']
    original_format = original_format.lower()

    if original_format not in supported_formats:
        raise ValueError(f"{original_format} not supported!")

    try:
        compressed_image = Image.open(BytesIO(compressed_data))
        decompressed_image = compressed_image

        # Convert to RGB color mode for color images
        if decompressed_image.mode not in ['1', 'L', 'RGB', 'RGBA']:
            decompressed_image = decompressed_image.convert('RGB')

        # Save and reopen the image to ensure efficient decompression
        with BytesIO() as output:
            decompressed_image.save(output, format=original_format.upper())
            output.seek(0)
            decompressed_image = Image.open(output)
    except Exception as e:
        raise IOError("Error decompressing the image.") from e

    return decompressed_image


def decompressed_file(compressed_data, file_format):
    """
    Decompresses a compressed image data and returns the uncompressed image.

    Args:
        compressed_data (bytes): The compressed image data as a bytes object.
        original_format (str): The original format of the image ('png', 'jpeg', 'jpg', 'webp').

    Returns:
        PIL.Image.Image: The decompressed image as a PIL Image object.
    except:
        Exception as str(e)
    """
    try:
        with Image.open(BytesIO(compressed_data)) as image:
            # Convert to RGB color mode for color images
            if image.mode not in ['1', 'L', 'RGB', 'RGBA']:
                image = image.convert('RGB')

            # Create a new BytesIO buffer to store the decompressed image
            output_buffer = BytesIO()

            # Save the decompressed image to the output buffer
            image.save(output_buffer, format=file_format)

            # Reset the buffer position to the beginning
            output_buffer.seek(0)
    except Exception as e:
        return {'error': str(e)}, 400

    # Get the size of the output buffer
    buffer_size = output_buffer.getbuffer().nbytes

    # Return the decompressed image and additional information
    return output_buffer, buffer_size, 200, {'Content-Type': f'image/{file_format}'}
