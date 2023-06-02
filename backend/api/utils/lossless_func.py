import json
import numpy as np
import zlib
from ..utils.custom_jsonencoder import MyEncoder


def divide_into_blocks(image, block_size):
    height, width, _ = image.shape
    num_blocks_h = height // block_size
    num_blocks_w = width // block_size

    blocks = []
    for i in range(num_blocks_h):
        for j in range(num_blocks_w):
            block = image[i * block_size: (i + 1) * block_size,
                          j * block_size: (j + 1) * block_size]
            blocks.append(block)

    return blocks


def apply_predictive_coding(blocks):
    transformed_blocks = []
    for block in blocks:
        transformed_block = np.diff(block.astype(np.int16), axis=0)
        transformed_blocks.append(transformed_block)

    return transformed_blocks


def run_length_encode(data):
    encoded_data = []
    for block in data:
        flattened_block = block.flatten()
        encoded_block = []
        count = 1
        for i in range(1, len(flattened_block)):
            if flattened_block[i] == flattened_block[i - 1]:
                count += 1
            else:
                encoded_block.append((flattened_block[i - 1], count))
                count = 1
        encoded_block.append((flattened_block[-1], count))
        encoded_data.append(encoded_block)

    return {'encoded_data': encoded_data}


def compress_lossless(image, compression_settings):
    block_size = compression_settings.get('block_size', 8)
    blocks = divide_into_blocks(image, block_size)

    transformed_blocks = apply_predictive_coding(blocks)

    encoded_data = run_length_encode(transformed_blocks)

    serialized_data = json.dumps(encoded_data, cls=MyEncoder)

    try:
        compressed_data = zlib.compress(serialized_data.encode('utf-8'))
    except zlib.error:
        # Handle zlib compression error
        raise ValueError("Failed to compress data")

    return compressed_data
