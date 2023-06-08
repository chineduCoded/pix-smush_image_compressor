from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..models.image import ImageBlob


def fetch_compressed_image_data(image_id):
    """Fetches the compressed image data"""

    try:
        response = ImageBlob.query.filter_by(image_id=image_id).first()
        if response:
            original_filename = response.file_name
            compressed_data = response.compressed_data
            return original_filename, compressed_data
        else:
            return None, None
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)})
    except Exception as e:
        return jsonify({"error": str(e)})
