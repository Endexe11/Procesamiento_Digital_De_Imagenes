# Si ves "ModuleNotFoundError: No module named 'cv2'", instala OpenCV ejecutando:
# pip install opencv-python

import cv2
import numpy as np
import sys
import os

if len(sys.argv) < 3:
    print("Uso: python segment_leaf.py <ruta_imagen> <ruta_salida>")
    sys.exit(1)

image_path = sys.argv[1]
output_path = sys.argv[2]

print(f"Intentando leer: {image_path}")
print(f"Existe el archivo? {os.path.exists(image_path)}")
print(f"Tamaño del archivo: {os.path.getsize(image_path) if os.path.exists(image_path) else 'No existe'}")

image = cv2.imread(image_path)
if image is None:
    print("No se pudo leer la imagen.")
    sys.exit(1)

# Convertir a espacio HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# --- Rangos HSV ajustables ---
# Puedes ajustar estos valores según tus imágenes
lower_green = np.array([40, 60, 40])
upper_green = np.array([80, 255, 255])
lower_yellow = np.array([15, 30, 30])
upper_yellow = np.array([40, 255, 255])
lower_brown = np.array([8, 40, 20])
upper_brown = np.array([30, 255, 180])

# Crear máscaras individuales
mask_green = cv2.inRange(hsv, lower_green, upper_green)
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)

# Combinar todas las máscaras
mask = cv2.bitwise_or(mask_green, mask_yellow)
mask = cv2.bitwise_or(mask, mask_brown)

# --- Operaciones morfológicas avanzadas ---
kernel = np.ones((7, 7), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)  # Cierra huecos internos
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)   # Elimina ruido externo
mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)             # Resalta bordes

# --- Eliminación automática de fondo ---
# Encuentra el contorno más grande (la hoja)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if not contours:
    print("No se encontró la hoja.")
    sys.exit(1)
leaf_contour = max(contours, key=cv2.contourArea)
mask_leaf = np.zeros_like(mask)
cv2.drawContours(mask_leaf, [leaf_contour], -1, 255, thickness=cv2.FILLED)

# Aplica la máscara de la hoja a la imagen original
result = cv2.bitwise_and(image, image, mask=mask_leaf)

# Fondo negro automático
background = np.zeros_like(image)
final = np.where(mask_leaf[..., None] == 255, result, background)

# Guardar la imagen segmentada
cv2.imwrite(output_path, final)