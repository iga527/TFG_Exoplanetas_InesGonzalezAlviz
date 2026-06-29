# -*- coding: utf-8 -*-
"""
Distribucion_Teq_Equilibrio.py
Distribución de temperaturas de equilibrio (T_eq)
del catálogo de exoplanetas confirmados (NASA Exoplanet Archive).

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import rcParams

# ── Configuración tipográfica ────────────────────────────────────────────────
rcParams['font.family']      = 'serif'
rcParams['mathtext.fontset'] = 'dejavuserif'
rcParams['font.size']        = 11

# ── Carga de datos ───────────────────────────────────────────────────────────
RUTA_CSV = 'planetas.csv'   # ajustar si el script está en otro directorio
df  = pd.read_csv(RUTA_CSV, comment='#')
teq = df['pl_eqt'].dropna()            # temperatura de equilibrio [K]
N   = len(teq)                          # planetas con T_eq medida
T_med = float(np.median(teq))           # mediana [K]

# ── Figura ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4.5))

# Histograma principal: 70 bins lineales en [0, 3000] K
counts, bins_e, _ = ax.hist(
    teq, bins=70, range=(0, 3000),
    color='lightblue', alpha=0.82,
    edgecolor='white', linewidth=0.4
)
ymax = counts.max()

# Reservamos espacio vertical para las anotaciones
ax.set_ylim(0, ymax * 1.28)

# ── Líneas de referencia ─────────────────────────────────────────────────────
# 1) Tierra: T_eq ≈ 255 K (A_B=0.30, redistribución global completa)
ax.axvline(255, color='#2d6a4f', linestyle='--', linewidth=1.6, zorder=3)
ax.text(190, ymax * 1.275,
        'Tierra\n$T_\\mathrm{eq}\\approx 255$ K',
        color='#2d6a4f', fontsize=10.5,
        ha='center', va='bottom', linespacing=1.4)

# 2) Límite orientativo de habitabilidad superficial (~500 K):
#    por encima de este umbral el efecto invernadero desbocado
#    puede impedir la estabilidad del agua líquida.
ax.axvline(500, color='#c1121f', linestyle=':', linewidth=1.7, zorder=3)
ax.text(528, ymax * 1.29,
        'Límite\nhabitabilidad',
        color='#c1121f', fontsize=10.5,
        ha='center', va='bottom', linespacing=1.4)

# 3) Mediana de la muestra detectada
ax.axvline(T_med, color='navy', linestyle=(0, (4, 3)), linewidth=1.5, zorder=3)
ax.text(T_med, ymax * 1.29,
        f'Mediana\n{T_med:.0f}' + r' K',
        color='navy', fontsize=10.5,
        ha='center', va='bottom', linespacing=1.4)

# ── Anotación de tamaño muestral ─────────────────────────────────────────────
# Se usa espacio fino (\,) como separador de miles (convención científica europea)
miles = N // 1000
resto = N %  1000
ax.text(0.98, 0.96,
        f'$N = {miles}\\,{resto:03d}$',
        transform=ax.transAxes,
        ha='right', va='top',
        fontsize=11, color='dimgray')

# ── Ejes y estética ──────────────────────────────────────────────────────────
ax.set_xlabel(r'Temperatura de equilibrio $T_\mathrm{eq}$ (K)', fontsize=12)
ax.set_ylabel('Número de planetas', fontsize=12)
ax.set_xlim(0, 3000)
ax.tick_params(axis='both', labelsize=10)
ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(5))
ax.yaxis.set_minor_locator(mticker.AutoMinorLocator())
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

RUTA_SALIDA = 'Distribucion_Teq_Equilibrio.png'
plt.savefig(RUTA_SALIDA, dpi=200, bbox_inches='tight')
plt.show()
plt.close()

print(f"Guardado: {RUTA_SALIDA}")






print(f"  N = {N}, mediana T_eq = {T_med:.0f} K, barra más alta = {ymax:.0f} planetas")
