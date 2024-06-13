import cv2

# Muestra la imagen en una ventana emergente

# Carga la imagen desde el archivo (reemplaza 'nombre_de_la_imagen.jpg' con el nombre de tu imagen)
image_path = 'GUANTES.jpg'
image = cv2.imread(image_path)

# Muestra la imagen en una ventana emergente
cv2.imshow('Imagen', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# IMAGEN A ESCALA DE GRISES

# Carga la imagen desde el archivo (reemplaza 'nombre_de_la_imagen.jpg' con el nombre de tu imagen)
image_path = 'GUANTES.jpg'
image = cv2.imread(image_path)

# Convierte la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detecta bordes utilizando el algoritmo de Canny
edges = cv2.Canny(gray_image, 100, 200)  # Ajusta los valores según sea necesario


# Muestra los bordes detectados en una ventana emergente

cv2.imshow('Bordes Detectados', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# o	Muestra la imagen con los contornos dibujados en una ventana emergente

# Carga la imagen desde el archivo (reemplaza 'nombre_de_la_imagen.jpg' con el nombre de tu imagen)
image_path = 'GUANTES.jpg'
image = cv2.imread(image_path)

# Convierte la imagen a escala de grises
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detecta bordes utilizando el algoritmo de Canny
edges = cv2.Canny(gray_image, 100, 200)  # Ajusta los valores según sea necesario

# Encuentra los contornos en la imagen
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibuja los contornos en la imagen original
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)  # Color verde, grosor 2

# Muestra la imagen con los contornos dibujados en una ventana emergente
cv2.imshow('Contornos Detectados', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Guardar Imagen con contorno

def guardar_contornos(imagen, contornos, nombre_archivo):
    # Dibuja los contornos en la imagen original
    imagen_contornos = imagen.copy()
    cv2.drawContours(imagen_contornos, contornos, -1, (0, 255, 0), 2)

    # Guarda la imagen con contornos en un archivo nuevo
    cv2.imwrite(nombre_archivo, imagen_contornos)
    print(f"Imagen con contornos guardada como {nombre_archivo}")

# Ejemplo de uso:
if __name__ == "__main__":
    # Carga una imagen (reemplaza con tu propia imagen)
    imagen_original = cv2.imread("GUANTES.jpg", cv2.IMREAD_COLOR)

    # Detecta los contornos en la imagen (reemplaza con tu propio método de detección)
    contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Guarda la imagen con contornos en un archivo nuevo
    guardar_contornos(imagen_original, contornos, "GUANTES2.jpg")


