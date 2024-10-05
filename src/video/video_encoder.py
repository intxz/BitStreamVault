import cv2
import numpy as np
from utils.algorithms import (
    compress_frame_dct,
    decompress_frame_dct,
)  # Importar el algoritmo de optimización


def bits_to_video(bits, width=256, height=144, output_file="output_video.mp4"):
    """Convierte los bits en un video donde cada frame representa una porción de bits."""
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, 30.0, (width, height), isColor=False)

    total_bits = len(bits)
    frame_size = width * height

    # Convertir la longitud de los bits originales a una secuencia de 32 bits
    num_bits_originales = format(total_bits, "032b")
    bits_num_originales = [int(bit) for bit in num_bits_originales]

    # Añadir el número de bits originales al inicio de los bits
    bits_with_extension = bits_num_originales + bits

    # Si el total de bits no es múltiplo del tamaño del frame, rellenamos con ceros
    if len(bits_with_extension) % frame_size != 0:
        padding = frame_size - (len(bits_with_extension) % frame_size)
        bits_with_extension = np.concatenate(
            [bits_with_extension, np.zeros(padding, dtype=np.uint8)]
        )

    total_bits = len(bits_with_extension)
    print(
        f"Bits a escribir en el video (con padding si aplica): {bits_with_extension[:32]}..."
    )

    for i in range(0, total_bits, frame_size):
        frame_bits = bits_with_extension[i : i + frame_size]

        # Convertir los bits en una imagen de 0 y 255 (blanco y negro)
        frame = (np.array(frame_bits).reshape((height, width)) * 255).astype(np.uint8)

        # Escribir el frame en el vídeo
        out.write(frame)

    out.release()
    print(f"Video guardado como: {output_file}")
