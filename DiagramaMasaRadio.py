# -*- coding: utf-8 -*-
"""
Diagrama Masa-Radio Final
Cobertura completa de datos y curvas teóricas restringidas
a su rango de validez física.

"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D

# ─── 1. CARGA ────────────────────────────────────────────────────────────────

plt.close('all')
df = pd.read_csv('planetas.csv', comment='#')

# ─── 2. CLASIFICACIÓN DE DATOS ───────────────────────────────────────────────

# Partición primaria: ¿el radio fue medido directamente?
con_radio_medido = df['pl_radeerr1'].notna()

# Grupo A: radio medido + masa medida directamente, con error conocido
calidad_mask = (
    con_radio_medido
    & (df['pl_bmassprov'] == 'Mass')
    & df['pl_bmasseerr1'].notna()
)
df_calidad = df[calidad_mask].copy()

# Grupo D: radio medido + masa mínima (Msini), con error conocido
msini_mask = (
    con_radio_medido
    & (df['pl_bmassprov'] == 'Msini')
    & df['pl_bmasseerr1'].notna()
)
df_msini = df[msini_mask].copy()

# Grupo B: radio medido, pero la masa no tiene barra de error fiable
# (con frecuencia porque procede de una relación masa-radio empírica
# en lugar de una medida espectroscópica independiente).
otros_mask = con_radio_medido & ~calidad_mask & ~msini_mask
df_otros = df[otros_mask].copy()

# Grupo C: radio no medido; el catálogo lo estima mediante el modelo
# empírico de Chen & Kipping a partir de la masa. La masa suele ser
# una medida directa (velocidad radial), aunque el radio es estimado.
imputados_mask = ~con_radio_medido
df_imputados = df[imputados_mask].copy()

assert (
    calidad_mask.sum() + msini_mask.sum()
    + otros_mask.sum() + imputados_mask.sum()
) == len(df), "Los grupos no cubren el total de filas: revisar la lógica de clasificación."

# ─── 3. ESTILO ───────────────────────────────────────────────────────────────

plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'font.family':      'serif',
    'font.size':        11,
    'axes.labelsize':   12,
    'axes.titlesize':   14,
    'xtick.labelsize':  11,
    'ytick.labelsize':  11,
    'legend.fontsize':   9,
})

# ─── 4. FIGURA ───────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(14, 9))

# Función auxiliar: scatter con barras de error asimétricas
def plot_with_errors(axis, dataframe, color, label, alpha_point=0.6):
    """
    Dibuja puntos con barras de error asimétricas. Se usa para los grupos
    con incertidumbres reportadas en ambos parámetros (masa y radio).
    """
    x_err = [np.abs(dataframe['pl_bmasseerr2']), dataframe['pl_bmasseerr1']]
    y_err = [np.abs(dataframe['pl_radeerr2']),   dataframe['pl_radeerr1']]
    axis.errorbar(
        dataframe['pl_bmasse'], dataframe['pl_rade'],
        xerr=x_err, yerr=y_err,
        fmt='o', markersize=3, color=color, ecolor=color,
        elinewidth=0.5, capsize=0, alpha=alpha_point, label=label,
        markeredgecolor='none'
    )

# ─── 5. DATOS DE EXOPLANETAS ─────────────────────────────────────────────────
# Orden de dibujo (= orden en la leyenda): de mayor a menor calidad
# observacional, terminando con las masas mínimas.

plot_with_errors(ax, df_calidad, 'lightblue',
                 'Masa medida y radio medido')

ax.scatter(df_otros['pl_bmasse'], df_otros['pl_rade'],
           color='mediumorchid', alpha=0.35, s=6,
           label='Radio medido y masa estimada', zorder=2)

ax.scatter(df_imputados['pl_bmasse'], df_imputados['pl_rade'],
           color='darkgray', alpha=0.1, s=5,
           label='Radio estimado y masa medida', zorder=1)

plot_with_errors(ax, df_msini, 'red',
                 r'Masa mínima ($M_p \sin i$) y radio medido')

# ─── 6. MODELOS TEÓRICOS ─────────────────────────────────────────────────────
# Restringidos a M ≤ 200 M⊕: más allá, la ecuación de estado de
# materiales condensados deja de describir la composición dominante
# (envolturas de H/He), como se discute en el Capítulo 3.

M_MAX_TEORICA = 200
m_teorica = np.logspace(-1.2, np.log10(M_MAX_TEORICA), 500)

ax.plot(m_teorica, 0.70 * (m_teorica**0.27), '--',
        color='darkorange',   alpha=0.8, label='100% Hierro',          zorder=10)
ax.plot(m_teorica, 1.00 * (m_teorica**0.27), '-',
        color='saddlebrown',  lw=2,      label='Composición terrestre', zorder=11)
ax.plot(m_teorica, 1.25 * (m_teorica**0.27), '--',
        color='darkblue',     alpha=0.8, label='100% Agua/Hielo',       zorder=12)

# ─── 7. ESTÉTICA Y LÍMITES ───────────────────────────────────────────────────

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'Masa ($M_{\oplus}$)', fontsize=12)
ax.set_ylabel(r'Radio ($R_{\oplus}$)', fontsize=12)
ax.set_title('Diagrama Masa-Radio con Barras de Error e Incertidumbre',
             fontweight='bold', fontsize=14)
ax.set_xlim(0.07, 15000)
ax.set_ylim(0.4, 35)

# ─── 8. SISTEMA SOLAR ────────────────────────────────────────────────────────

ss_planets = {
    'Tierra':  [1.0,    1.0],
    'Venus':   [0.815,  0.949],
    'Marte':   [0.107,  0.533],
    'Neptuno': [17.14,  3.88],
    'Urano':   [14.53,  4.01],
    'Júpiter': [317.8,  11.2],
    'Saturno': [95.16,  9.45],
}

text_offsets = {
    'Tierra':  (1.2, 0.95),
    'Venus':   (1.2, 0.85),
    'Marte':   (1.1, 0.90),
    'Neptuno': (1.2, 0.90),
    'Urano':   (0.7, 1.10),
    'Júpiter': (1.2, 1.00),
    'Saturno': (1.2, 0.90),
}

for nombre, datos in ss_planets.items():
    ax.scatter(datos[0], datos[1], marker='X', color='red', s=120,
               zorder=100, edgecolors='black', linewidth=1.0)
    ox, oy = text_offsets.get(nombre, (1.2, 1.0))
    txt = ax.text(datos[0] * ox, datos[1] * oy, nombre,
                  fontsize=11, fontweight='bold', color='black', zorder=101)
    txt.set_path_effects([
        patheffects.withStroke(linewidth=3, foreground='white')
    ])

# ─── 9. LEYENDA ──────────────────────────────────────────────────────────────
# Se construye explícitamente por etiqueta para garantizar el orden
# deseado con independencia del orden de dibujo:
#   (1) exoplanetas de mayor a menor calidad observacional,
#   (2) líneas de referencia de composición,
#   (3) Sistema Solar.

all_handles, all_labels = ax.get_legend_handles_labels()
by_label = dict(zip(all_labels, all_handles))

desired_order = [
    'Masa medida y radio medido',
    'Radio medido y masa estimada',
    'Radio estimado y masa medida',
    r'Masa mínima ($M_p \sin i$) y radio medido',
    '100% Hierro',
    'Composición terrestre',
    '100% Agua/Hielo',
]
ordered_handles = [by_label[lbl] for lbl in desired_order]

ss_handle = Line2D([0], [0], marker='X', color='black',
                   markerfacecolor='red', markersize=10,
                   label='Sistema Solar', linewidth=0)
ordered_handles.append(ss_handle)

ax.legend(handles=ordered_handles, loc='upper left', fontsize=9, frameon=True)

# ─── 10. EXPORTACIÓN ─────────────────────────────────────────────────────────

plt.savefig('Diagrama_MR_Final_TFG.png', dpi=300, bbox_inches='tight')
plt.show()

print(
    "Figura guardada. Grupos: calidad=%d, msini=%d, otros=%d, imputados=%d "
    "(suma=%d, total=%d)" % (
        calidad_mask.sum(), msini_mask.sum(),
        otros_mask.sum(),   imputados_mask.sum(),
        calidad_mask.sum() + msini_mask.sum()
        + otros_mask.sum() + imputados_mask.sum(),
        len(df)
    )
)
