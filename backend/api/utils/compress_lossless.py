import cv2
import heapq
import numpy as np
import base64


def compress_image(image_data, grayscale=True, quality=100):
    """ Compresses an image using OpenCV and Huffman coding technique.

    Args:
        image_data (bytes): The image data to compress.
        grayscale (bool): Whether to convert the image to grayscale before compression. Default is True.
        quality (int): The quality of the compressed image, from 0 to 100. Default is 100.

    Returns:
        str: The base64-encoded string representation of the compressed image data.
    """
    # Read the image data
    image = cv2.imdecode(np.frombuffer(
        image_data, np.uint8), cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if grayscale else image

    # Calculate the frequency of each pixel value
    freq = {}
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i, j] in freq:
                freq[gray[i, j]] += 1
            else:
                freq[gray[i, j]] = 1

    # Build the Huffman tree
    heap = [[freq[key], [key, ""]] for key in freq]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])

    # Generate the Huffman codes for each pixel value
    codes = {}
    for pair in heap[0][1:]:
        codes[pair[0]] = pair[1]

    # Compress the image using Huffman coding
    compressed = ""
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            compressed += codes[gray[i, j]]

    # Pad the compressed data to a multiple of 8 bits
    while len(compressed) % 8 != 0:
        compressed += '0'

    # Convert the compressed data to bytes
    compressed_bytes = bytearray()
    for i in range(0, len(compressed), 8):
        compressed_bytes.append(int(compressed[i:i+8], 2))

    # Compress the bytes using OpenCV
    params = [cv2.IMWRITE_PNG_COMPRESSION, quality]
    _, compressed_image = cv2.imencode('.png', np.array(
        compressed_bytes), params)

    # Convert the compressed image data to a base64-encoded string
    compressed_base64 = base64.b64encode(
        compressed_image.tobytes()).decode('utf-8')

    return compressed_base64
