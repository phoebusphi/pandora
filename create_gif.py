import os
from PIL import Image


def create_gif(image_folder, gif_filename, duration=500):
    """
    Convierte imágenes JPG de una carpeta en un GIF animado.

    Parámetros:
    - image_folder: Ruta de la carpeta con las imágenes
    - gif_filename: Nombre del archivo GIF de salida
    - duration: Tiempo de visualización de cada imagen en milisegundos (por defecto 500)
    """
    # Obtener lista de archivos de imagen, ordenados alfabéticamente
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
    images.sort()  # Ordenar para asegurar secuencia consistente

    # Lista para almacenar los frames
    frames = []

    # Abrir y procesar cada imagen
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        img = Image.open(image_path)

        # Convertir a modo RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')

        frames.append(img)

    # Guardar el GIF
    frames[0].save(
        gif_filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0  # 0 significa bucle infinito
    )

    print(f"GIF creado exitosamente: {gif_filename}")

# Ejemplo de uso

# Reemplaza 'ruta/a/tu/carpeta/de/imagenes' con la ruta real de tus imágenes
create_gif('./images_gif/', 'output.gif')
