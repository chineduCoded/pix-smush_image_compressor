from flask import current_app
from .. import db
from ..models.image import ImageBlob
import os
import time
import random
import string


def generate_unique_filename():
    timestamp = str(int(time.time()))  # Get the current timestamp
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8))  # Generate a random string
    # Combine timestamp and random string
    filename = timestamp + '_' + random_string
    return filename


def save_large_data(file):
    filename = generate_unique_filename()
    filepath = os.path.join(current_app.config['IMAGE_DIRECTORY'], filename)
    file.save(filepath)
    return filename, filepath


def store_large_data(file):
    filename, filepath = save_large_data(file)
    large_data = ImageBlob(filename=filename, filepath=filepath)
    db.session.add(large_data)
    db.session.commit()
    return large_data
