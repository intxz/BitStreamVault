import numpy as np
from scipy.fftpack import dct, idct


QUANTIZATION_MATRIX = np.array(
    [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99],
    ]
)


def block_dct(image_block):
    """Aplica la DCT a un bloque de la imagen."""
    return dct(dct(image_block.T, norm="ortho").T, norm="ortho")


def block_idct(dct_block):
    """Aplica la IDCT para restaurar el bloque original."""
    return idct(idct(dct_block.T, norm="ortho").T, norm="ortho")


def compress_frame_dct(frame, block_size=8):
    """Aplica compresión DCT y cuantización a cada bloque de la imagen del frame."""
    h, w = frame.shape
    dct_frame = np.zeros_like(frame, dtype=np.float32)

    # Dividir la imagen en bloques y aplicar DCT
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = frame[i : i + block_size, j : j + block_size]
            dct_block = block_dct(block)
            # Cuantizar el bloque DCT
            quantized_block = (
                np.round(dct_block / QUANTIZATION_MATRIX) * QUANTIZATION_MATRIX
            )
            dct_frame[i : i + block_size, j + j + block_size] = quantized_block

    return dct_frame


def decompress_frame_dct(dct_frame, block_size=8):
    """Aplica la descompresión (IDCT) para restaurar el frame original."""
    h, w = dct_frame.shape
    decompressed_frame = np.zeros_like(dct_frame, dtype=np.float32)

    # Dividir en bloques y aplicar IDCT
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = dct_frame[i : i + block_size, j + j + block_size]
            decompressed_frame[i : i + block_size, j + j + block_size] = block_idct(
                block
            )

    return np.clip(decompressed_frame, 0, 255).astype(np.uint8)
