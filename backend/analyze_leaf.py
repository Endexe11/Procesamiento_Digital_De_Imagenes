import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import os

if len(sys.argv) < 3:
    print("Uso: python analyze_leaf.py <ruta_imagen_segmentada> <ruta_histograma>")
    sys.exit(1)

image_path = sys.argv[1]
hist_path = sys.argv[2]

image = cv2.imread(image_path)
if image is None:
    print("No se pudo leer la imagen segmentada.")
    sys.exit(1)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
mask = cv2.inRange(image_rgb, (1,1,1), (255,255,255))  # Considera todo lo que no es negro como hoja

r_vals = image_rgb[:,:,0][mask > 0]
g_vals = image_rgb[:,:,1][mask > 0]
b_vals = image_rgb[:,:,2][mask > 0]

plt.figure(figsize=(10, 4))
plt.hist(r_vals, bins=256, color='r', alpha=0.5, label='Red')
plt.hist(g_vals, bins=256, color='g', alpha=0.5, label='Green')
plt.hist(b_vals, bins=256, color='b', alpha=0.5, label='Blue')
plt.title('Histograma de colores - Hoja de naranjo')
plt.xlabel('Intensidad')
plt.ylabel('Frecuencia')
plt.legend()
plt.tight_layout()
plt.savefig(hist_path)
plt.close()

# Calcular estadísticas
mean_r = np.mean(r_vals)
mean_g = np.mean(g_vals)
mean_b = np.mean(b_vals)
std_r = np.std(r_vals)
std_g = np.std(g_vals)
std_b = np.std(b_vals)

# Análisis básico basado en reglas simples
analysis = ""
if mean_g > mean_r and mean_g > mean_b and mean_g > 80:
    analysis = "Verde sano: Dominancia del canal verde (G) con valores en rango medio-alto."
elif mean_r > 100 and mean_g > 100 and mean_b < 80:
    analysis = "Clorosis: Elevación de R y G pero baja en B. Posible deficiencia de N, Mg o Fe."
elif mean_r > 120 and mean_g < 80 and mean_b < 80:
    analysis = "Necrosis o quemaduras: Pico alto en R y disminución marcada en G y B."
elif mean_r < 60 and mean_g < 60 and mean_b < 60:
    analysis = "Hongos o enfermedades fúngicas: Presencia de manchas oscuras o negras."
else:
    analysis = "No se puede determinar claramente el estado. Revisa el histograma para más detalles."

# --- Cálculo de proporciones de color ---
# Leer la imagen segmentada en HSV
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Rango para verde, amarillo y marrón (debe coincidir con segment_leaf.py)
lower_green = np.array([25, 40, 40])
upper_green = np.array([90, 255, 255])
lower_yellow = np.array([15, 40, 40])
upper_yellow = np.array([35, 255, 255])
lower_brown = np.array([10, 60, 20])
upper_brown = np.array([25, 255, 200])

mask_green = cv2.inRange(image_hsv, lower_green, upper_green)
mask_yellow = cv2.inRange(image_hsv, lower_yellow, upper_yellow)
mask_brown = cv2.inRange(image_hsv, lower_brown, upper_brown)
mask_total = cv2.bitwise_or(mask_green, mask_yellow)
mask_total = cv2.bitwise_or(mask_total, mask_brown)

total_pixels = np.count_nonzero(mask_total)
green_pixels = np.count_nonzero(mask_green)
yellow_pixels = np.count_nonzero(mask_yellow)
brown_pixels = np.count_nonzero(mask_brown)

green_ratio = green_pixels / total_pixels if total_pixels else 0
yellow_ratio = yellow_pixels / total_pixels if total_pixels else 0
brown_ratio = brown_pixels / total_pixels if total_pixels else 0

# --- Estadísticas HSV ---
h_vals = image_hsv[:,:,0][mask_total > 0]
s_vals = image_hsv[:,:,1][mask_total > 0]
v_vals = image_hsv[:,:,2][mask_total > 0]

mean_h = np.mean(h_vals) if h_vals.size else 0
mean_s = np.mean(s_vals) / 255 if s_vals.size else 0
mean_v = np.mean(v_vals) / 255 if v_vals.size else 0
std_h = np.std(h_vals) if h_vals.size else 0
std_s = np.std(s_vals) / 255 if s_vals.size else 0
std_v = np.std(v_vals) / 255 if v_vals.size else 0

# --- Diagnóstico mejorado basado en proporciones y HSV ---
if green_ratio > 0.85 and yellow_ratio < 0.10 and brown_ratio < 0.05:
    diagnosis = "Hoja completamente sana"
    explanation = "La hoja es casi totalmente verde, sin señales de daño ni clorosis."
elif green_ratio > 0.7 and yellow_ratio < 0.15 and brown_ratio < 0.10:
    diagnosis = "Hoja mayormente sana"
    explanation = "Predomina el verde, pero hay pequeñas zonas amarillas o marrones. Vigilar posibles inicios de daño."
elif yellow_ratio >= 0.15 and yellow_ratio < 0.30 and brown_ratio < 0.10:
    diagnosis = "Clorosis leve"
    explanation = "Presencia moderada de amarillo, posible deficiencia de nutrientes. Recomendable monitorear."
elif yellow_ratio >= 0.30 and brown_ratio < 0.15:
    diagnosis = "Clorosis severa"
    explanation = "Gran parte de la hoja es amarilla, lo que indica deficiencia nutricional avanzada."
elif brown_ratio >= 0.10 and brown_ratio < 0.25:
    diagnosis = "Necrosis leve o daño por sequía"
    explanation = "Zonas marrones detectadas, posible inicio de necrosis o daño físico."
elif brown_ratio >= 0.25:
    diagnosis = "Necrosis severa"
    explanation = "La hoja presenta grandes áreas marrones, indicando daño severo, necrosis o quemaduras."
elif mean_v < 0.25 and brown_ratio < 0.10:
    diagnosis = "Posible presencia de hongos o manchas oscuras"
    explanation = "La hoja tiene muchas zonas oscuras, lo que puede indicar enfermedades fúngicas."
elif green_ratio < 0.5 and yellow_ratio > 0.25 and brown_ratio > 0.15:
    diagnosis = "Hoja en mal estado general"
    explanation = "Predominan los colores amarillo y marrón, la hoja está muy dañada."
else:
    diagnosis = "No se puede determinar claramente el estado"
    explanation = "Revisa el histograma y las proporciones de color para más detalles."

# --- Cálculo de área y perímetro foliar ---
leaf_area_px = np.count_nonzero(mask_total)
contours, _ = cv2.findContours(mask_total, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
leaf_perimeter_px = sum(cv2.arcLength(cnt, True) for cnt in contours)

# (Opcional) Guardar imagen con contorno
contour_img = image.copy()
cv2.drawContours(contour_img, contours, -1, (255, 0, 0), 2)
cv2.imwrite(image_path.replace('.jpg', '_contorno.jpg'), contour_img)

# --- Guardar el análisis en un archivo de texto ---
analysis_path = hist_path.replace('.jpg', '_analisis.txt')
with open(analysis_path, 'w', encoding='utf-8') as f:
    f.write("Análisis cromático automático de la hoja\n")
    f.write("="*40 + "\n\n")
    f.write(f"Proporción verde:   {green_ratio*100:.1f}%\n")
    f.write(f"Proporción amarillo:{yellow_ratio*100:.1f}%\n")
    f.write(f"Proporción marrón:  {brown_ratio*100:.1f}%\n\n")
    f.write(f"Área foliar (píxeles): {leaf_area_px}\n")
    f.write(f"Perímetro foliar (píxeles): {leaf_perimeter_px:.1f}\n\n")
    f.write(f"Promedio R: {mean_r:.2f}   Desv: {std_r:.2f}\n")
    f.write(f"Promedio G: {mean_g:.2f}   Desv: {std_g:.2f}\n")
    f.write(f"Promedio B: {mean_b:.2f}   Desv: {std_b:.2f}\n\n")
    f.write(f"Promedio H: {mean_h:.2f}   Desv: {std_h:.2f}\n")
    f.write(f"Promedio S: {mean_s:.2f}   Desv: {std_s:.2f}\n")
    f.write(f"Promedio V: {mean_v:.2f}   Desv: {std_v:.2f}\n\n")
    f.write(f"Diagnóstico: {diagnosis}\n")
    f.write(f"Explicación: {explanation}\n")

# Datos para la tabla
table_data = [
    ["Proporción verde", f"{green_ratio*100:.1f} %"],
    ["Proporción amarillo", f"{yellow_ratio*100:.1f} %"],
    ["Proporción marrón", f"{brown_ratio*100:.1f} %"],
    ["Área foliar (px)", f"{leaf_area_px}"],
    ["Perímetro foliar (px)", f"{leaf_perimeter_px:.1f}"],
    ["Promedio R", f"{mean_r:.2f}"],
    ["Promedio G", f"{mean_g:.2f}"],
    ["Promedio B", f"{mean_b:.2f}"],
    ["Promedio H", f"{mean_h:.2f}"],
    ["Promedio S", f"{mean_s:.2f}"],
    ["Promedio V", f"{mean_v:.2f}"],
    ["Desv. R", f"{std_r:.2f}"],
    ["Desv. G", f"{std_g:.2f}"],
    ["Desv. B", f"{std_b:.2f}"],
    ["Desv. H", f"{std_h:.2f}"],
    ["Desv. S", f"{std_s:.2f}"],
    ["Desv. V", f"{std_v:.2f}"],
    ["Diagnóstico", diagnosis],
    ["Explicación", explanation]
]

# Crear la figura de la tabla
fig, ax = plt.subplots(figsize=(8, len(table_data)*0.5 + 1))
ax.axis('off')
table = ax.table(cellText=table_data, colLabels=["Métrica", "Valor"], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

# Guardar la tabla como imagen
table_img_path = hist_path.replace('.jpg', '_tabla.png')
plt.tight_layout()
plt.savefig(table_img_path, bbox_inches='tight', dpi=200)
plt.close()

print(f"Diagnóstico: {diagnosis}")
print(f"Archivo de análisis guardado en: {analysis_path}")