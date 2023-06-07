import os
import tempfile
from PIL import Image


def get_compressed_size(compressed_data, file_extension):
    supported_extensions = ['.jpg', '.jpeg', '.png', '.webp']

    if file_extension not in supported_extensions:
        raise ValueError(
            f"{file_extension.lower()} unsupported file extension!")

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(compressed_data)
        temp_file_name = temp_file.name

    try:
        with Image.open(temp_file_name) as compressed_image:
            width, height = compressed_image.size
            compressed_image.save(temp_file_name)

        compressed_size = os.path.getsize(temp_file_name)
        os.remove(temp_file_name)

        return compressed_size

    except Exception as e:
        os.remove(temp_file_name)
        raise e
