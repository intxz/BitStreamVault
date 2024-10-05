from data.file_handler import FileHandler
from video.video_decoder import video_to_bits
import tkinter as tk
from tkinter import filedialog


def select_video():
    """Función que abre un diálogo para seleccionar un video."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    video_path = filedialog.askopenfilename(
        title="Selecciona un video para reconstruir el archivo"
    )
    return video_path


def main():
    # Selecciona el video usando Tkinter
    input_video = select_video()

    if not input_video:
        print("No se seleccionó ningún video")
        return

    # Extrae la extensión y los bits del video
    file_extension, extracted_bits = video_to_bits(input_video, width=256, height=144)
    print(f"Bits extraídos: {len(extracted_bits)} bits")
    print(f"Extensión de archivo: {file_extension}")

    if not file_extension:
        print("No se pudo extraer la extensión.")
        return

    # Asegúrate de que los bits extraídos estén alineados a 8 bits (si hay relleno, elimínalo)
    padding_size = len(extracted_bits) % 8
    if padding_size != 0:
        extracted_bits = extracted_bits[:-padding_size]

    # Crear el archivo de salida con la extensión original
    output_file = filedialog.asksaveasfilename(
        defaultextension=f".{file_extension}",
        title="Guardar archivo reconstruido",
        filetypes=[(f"Archivos {file_extension}", f"*.{file_extension}")],
    )

    # Inicializa el manejador de archivos para guardar el archivo reconstruido
    file_handler = FileHandler(output_file)

    # Reconstruir el archivo original a partir de los bits restantes
    file_handler.bits_to_file(extracted_bits, output_file)
    print(f"Archivo reconstruido y guardado en: {output_file}")


if __name__ == "__main__":
    main()
