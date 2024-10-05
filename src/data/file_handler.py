import os
import numpy as np


class FileHandler:

    def __init__(self, file_path):
        self.file_path = file_path

    def file_to_bits(self):
        with open(self.file_path, "rb") as file:
            byte_data = file.read()
            bit_array = np.unpackbits(np.frombuffer(byte_data, dtype=np.uint8))
        return bit_array

    def bits_to_file(self, bits, output_path):
        # Asegurarse de que los bits estén en la longitud adecuada para convertir a bytes
        byte_data = bytearray(
            int("".join(map(str, bits[i : i + 8])), 2) for i in range(0, len(bits), 8)
        )

        with open(output_path, "wb") as file:
            file.write(byte_data)
        print(f"File reconstructed and saved at: {output_path}")
