import cv2
import numpy as np


def video_to_bits(input_video, width=256, height=144):
    """Lee un video, extrae los bits representados en cada frame y extrae la extensión del archivo original."""
    cap = cv2.VideoCapture(input_video)
    bits = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el frame de 255/0 (blanco y negro) a 1/0 (bits)
        frame_bits = (frame[:, :, 0] > 128).astype(np.uint8).flatten()
        bits.extend(frame_bits)

    cap.release()

    # Convertir bits a un array
    bits = np.array(bits)

    # Extraer la longitud de los bits originales (primeros 32 bits)
    length_bits = bits[:32]
    original_length = int("".join(map(str, length_bits)), 2)

    # Extraer la extensión (siguientes 32 bits)
    extension_bits = bits[32:64]  # 32 bits para la extensión con delimitador
    extension_chars = [
        chr(int("".join(map(str, extension_bits[i : i + 8])), 2))
        for i in range(0, 32, 8)
    ]
    file_extension = "".join(extension_chars).replace(
        "\x00", ""
    )  # Eliminar el delimitador

    print(f"Bits extraídos del video (extensión): {extension_bits}")
    print(f"Extensión de archivo: {file_extension}")
    print(f"Longitud original de los bits: {original_length}")

    # Retornar la extensión y los bits restantes (ajustados a la longitud original)
    return file_extension, bits[64 : 64 + original_length]
