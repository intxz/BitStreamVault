from data.file_handler import FileHandler
from video.video_encoder import bits_to_video
import tkinter as tk
from tkinter import filedialog


def select_file():
    """Función que abre un diálogo para seleccionar un archivo."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo para convertir a video"
    )
    return file_path


def file_extension_to_bits(extension):
    """Convierte la extensión de archivo a una secuencia de 32 bits (4 caracteres, 8 bits por cada uno)."""
    extension = extension[:4].ljust(
        4, "\x00"
    )  # Asegurar que la extensión tenga exactamente 4 caracteres
    extension_bits = "".join(
        format(ord(char), "08b") for char in extension
    )  # Convertir cada carácter a 8 bits
    print(f"Extensión en bits ({extension.strip()}): {extension_bits}")
    return [int(bit) for bit in extension_bits]


def main():
    # Selecciona el archivo usando Tkinter
    input_file = select_file()

    if not input_file:
        print("No se seleccionó ningún archivo")
        return

    # Extraer la extensión del archivo original
    file_extension = input_file.split(".")[-1]
    print(f"Extensión del archivo: {file_extension}")

    # Inicializa el manejador de archivos
    file_handler = FileHandler(input_file)

    # Convierte el archivo a bits
    bits = file_handler.file_to_bits()
    print(f"Archivo convertido a {len(bits)} bits")

    # Convertir la extensión del archivo a bits y agregarla al principio del video
    extension_bits = file_extension_to_bits(file_extension)
    bits_with_extension = extension_bits + bits.tolist()

    # Imprimir la longitud total de los bits con la extensión
    print(f"Bits con la extensión añadida: {len(bits_with_extension)} bits")

    # Crear un vídeo a partir de los bits con la extensión
    bits_to_video(
        bits_with_extension, width=256, height=144, output_file="output_video.mp4"
    )
    print("Video generado a partir de los bits y extensión.")


if __name__ == "__main__":
    main()
