# -*- coding: utf-8 -*-
"""
Evolución temporal de Exoplanetas, añadiendo los hitos más importantes.


"""

import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el dataset de la NASA
# Asegúrate de que 'planetas.csv' esté en el mismo directorio que este script
# Se añade comment='#' porque a veces los CSV de la NASA incluyen un encabezado de metadatos
df = pd.read_csv('planetas.csv', comment='#')


# 2. Preparar los datos
# Filtramos para quedarnos con las columnas de interés y eliminamos nulos
df_plot = df[['disc_year', 'discoverymethod']].dropna()

# Contamos cuántos exoplanetas se descubrieron por año para cada método
conteo_anual = df_plot.groupby(['disc_year', 'discoverymethod']).size().unstack(fill_value=0)

# Calculamos la suma acumulativa a lo largo de los años
acumulado = conteo_anual.cumsum()

# Recortamos el DataFrame para mostrar desde 1990 en adelante
acumulado = acumulado[acumulado.index >= 1990]

# 3. Configurar el estilo de la gráfica
fig, ax = plt.subplots(figsize=(12, 6))

# Definimos los colores exactos de la imagen para los 4 métodos principales
colores = {
    'Transit': '#d62728',          # Rojo
    'Radial Velocity': '#1f77b4',  # Azul
    'Microlensing': '#2ca02c',     # Verde
    'Imaging': '#ff7f0e'           # Naranja
}

# Dibujamos las líneas principales
for metodo in acumulado.columns:
    if metodo in colores:
        ax.plot(acumulado.index, acumulado[metodo], marker='o', markersize=5,
                markerfacecolor='white', markeredgewidth=1.5,
                linewidth=2, color=colores[metodo], label=metodo)

# 4. Añadir los hitos históricos (líneas verticales)
hitos = [
    (1995, '51 Pegasi b\nPrimer exoplaneta en estrella solar'),
    (2009, 'Kepler\nLanzamiento Misión Kepler'),
    (2018, 'TESS\nLanzamiento Misión TESS')
]

for anio, texto in hitos:
    # Línea vertical punteada
    ax.axvline(x=anio, color='gray', linestyle='--', linewidth=1.2, alpha=0.8)
    # Texto alineado a la línea (usando transform para fijarlo en la parte superior)
    ax.text(anio + 0.3, 0.95, texto, transform=ax.get_xaxis_transform(),
            fontsize=9.7, verticalalignment='top', color='#333333')

# 5. Ajustes de formato y estética

ax.set_xlim(1990, 2025)
# Ajusta el límite superior según el número actual de tu CSV (aprox 5500+)
ax.set_ylim(0, acumulado.max().max() + 200) 
ax.set_title('Evolución Temporal Acumulativa de Exoplanetas', fontsize=16, fontweight='bold', pad=25)

# Cuadrícula
ax.grid(True, which='both', linestyle='-', color='#e0e0e0')

# Limpiar bordes para un aspecto más profesional e idéntico a tu referencia
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Leyenda
ax.legend(loc='upper left', frameon=False, fontsize=10)

plt.tight_layout()

# Guardar la figura en alta resolución para adjuntar al documento
plt.savefig('grafica_metodos_acumulados.png', dpi=300, bbox_inches='tight')







plt.show()