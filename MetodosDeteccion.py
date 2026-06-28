# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:03:07 2026

@author: Usuario
"""

#!/usr/bin/env python3
"""
Barras_Metodos_Deteccion.py
============================
Figura 6.1 del TFG: distribución de exoplanetas confirmados por método de
descubrimiento, representada como diagrama de barras horizontales en escala
logarítmica.

Motivación:
    La escala logarítmica permite visualizar simultáneamente el dominio del
    tránsito (73.4%, N=4523) y los métodos minoritarios (Cinemática de disco,
    N=1) sin comprometer la legibilidad. El eje X en escala log extiende el
    espacio visual hacia los métodos de baja representación.

    Los cuatro métodos principales (Tránsito, Velocidad radial, Microlentes,
    Imagen directa) se destacan en steelblue; los métodos secundarios se
    muestran en un tono más claro para priorizar visualmente la jerarquía.

Nota: el catálogo de la NASA Exoplanet Archive asigna UN único método
de descubrimiento por entrada, correspondiente al método de primera
confirmación. Muchos planetas han sido caracterizados posteriormente por
técnicas complementarias, pero esa información no está recogida en este campo.

Datos: planetas.csv (NASA Exoplanet Archive, N=6160).
Dependencias: pandas, matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import rcParams

# ── Configuración tipográfica ────────────────────────────────────────────────
rcParams['font.family']      = 'serif'
rcParams['mathtext.fontset'] = 'dejavuserif'
rcParams['font.size']        = 8.5

# ── Carga de datos ───────────────────────────────────────────────────────────
RUTA_CSV = 'planetas.csv'
df    = pd.read_csv(RUTA_CSV, comment='#')
total = len(df)

# ── Traducción de etiquetas al español ───────────────────────────────────────
TRADUCCION = {
    'Transit':                     'Tránsito',
    'Radial Velocity':             'Velocidad radial',
    'Microlensing':                'Microlentes grav.',
    'Imaging':                     'Imagen directa',
    'Transit Timing Variations':   'TTV',
    'Eclipse Timing Variations':   'ETV',
    'Orbital Brightness Modulation': 'Mod. de brillo',
    'Pulsar Timing':               'Temporiz. de púlsares',
    'Astrometry':                  'Astrometría',
    'Pulsation Timing Variations': 'Var. de pulsación',
    'Disk Kinematics':             'Cinemática de disco',
}

# Conteo y orden descendente
counts = df['discoverymethod'].value_counts()
labels = [TRADUCCION.get(m, m) for m in counts.index]
values = counts.values

# ── Colores ───────────────────────────────────────────────────────────────────
# Métodos principales (los cuatro primeros): steelblue más intenso
# Métodos secundarios: steelblue más claro
COLORES = ['orange' if i < 4 else 'lightblue' for i in range(len(values))]

# ── Figura ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 3.8))

bars = ax.barh(labels[::-1], values[::-1],   # invertir para que el mayor quede arriba
               color=COLORES[::-1], edgecolor='white', linewidth=0.5, height=0.65)

# ── Etiquetas de valor en cada barra ─────────────────────────────────────────
for i, (v, lab) in enumerate(zip(values[::-1], labels[::-1])):
    pct = 100 * v / total
    # Posición del texto: dentro de la barra si cabe, fuera si la barra es muy corta
    x_text = v * 1.15
    ax.text(x_text, i, f'{v:,}  ({pct:.2f}%)'.replace(',', '\u2009'),
            va='center', fontsize=10.5, color='#333333')

# ── Eje X: escala logarítmica ─────────────────────────────────────────────────
ax.set_xscale('log')
ax.set_xlim(0.5, 5e4)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x):,}'.replace(',', '\u2009') if x >= 1 else ''))
ax.set_xlabel('Número de planetas (escala logarítmica)', fontsize=11.5)

# ── Línea de separación visual entre métodos principales y secundarios ────────
# Los primeros 4 (índices 0-3) están en la parte superior; la separación
# visual cae entre el índice 3 y 4 del array invertido, es decir entre
# posición 6 y 7 del gráfico (ya que invertimos).
ax.axhline(len(values) - 4 - 0.5, color='gray', lw=0.7, ls='--', alpha=0.6)

# ── Estética ──────────────────────────────────────────────────────────────────
ax.tick_params(axis='both', labelsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.yaxis.set_tick_params(length=0)

plt.tight_layout()

RUTA_SALIDA = 'Barras_Metodos_Deteccion.png'
plt.savefig(RUTA_SALIDA, dpi=200, bbox_inches='tight')
plt.show()
plt.close()
print(f'Guardado: {RUTA_SALIDA}  (N total = {total})')