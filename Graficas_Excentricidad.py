# -*- coding: utf-8 -*-
"""
Distribución Masa-Distancia con barras de error

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# --- Configuración global de tamaño de fuente (aplicar antes de crear figuras) ---
plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'font.family': 'serif',
    'font.size': 14,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
})

# --- 1. Carga de datos ---
df = pd.read_csv('planetas.csv', comment='#')

# --- 2. Filtrado: planetas con errores en masa y semieje mayor disponibles ---
# Se elimina el filtro sobre pl_orbeccenerr1: no es necesario para este diagrama
df_err = df[
    (df['pl_bmasseerr1'].notna()) &
    (df['pl_orbsmaxerr1'].notna())
].copy()

# --- 3. Figura ---
fig, ax = plt.subplots(figsize=(12, 8))

# Barras de error asimétricas (err2 es negativo por convención → valor absoluto)
x_err = [
    np.abs(df_err['pl_orbsmaxerr2'].fillna(0)),
    df_err['pl_orbsmaxerr1'].fillna(0)
]
y_err = [
    np.abs(df_err['pl_bmasseerr2'].fillna(0)),
    df_err['pl_bmasseerr1'].fillna(0)
]

ax.errorbar(
    df_err['pl_orbsmax'], df_err['pl_bmasse'],
    xerr=x_err, yerr=y_err,
    fmt='o', markersize=2, color='royalblue', ecolor='gray',
    elinewidth=0.3, capsize=0, alpha=0.3,
    label='Exoplanetas confirmados'
)

# --- 4. Referencias del Sistema Solar ---
# Masas en M_Earth y semiejes en AU. Se usan annotate con conectores finos
# para separar etiquetas de Urano y Neptuno (masas similares, riesgo de solape).
ss_annotations = {
    'Tierra':  {'xy': (1.000,  1.0),    'xytext': (1.3,   1.0)},
    'Júpiter': {'xy': (5.203,  317.8),  'xytext': (6.8,   300.0)},
    'Saturno': {'xy': (9.537,  95.16),  'xytext': (12.0,  93.0)},
    'Urano':   {'xy': (19.19,  14.54),  'xytext': (12.3,  7.0)},
    'Neptuno': {'xy': (30.07,  17.15),  'xytext': (40.0,  15.0)},
}

for nombre, params in ss_annotations.items():
    ax.scatter(*params['xy'], color='red', marker='X', s=100, zorder=10)
    ax.annotate(
        nombre,
        xy=params['xy'],
        xytext=params['xytext'],
        fontweight='bold',
        color='black',
        fontsize=14,
        arrowprops=dict(arrowstyle='-', color='gray', lw=0.5)
    )

# Entrada de leyenda para el Sistema Solar
ax.scatter([], [], color='red', marker='X', s=100,
           label='Planetas del Sistema Solar')

# --- 5. Escala, etiquetas y guardado ---
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Semieje Mayor $a$ (UA)')
ax.set_ylabel('Masa $M_p$ ($M_{\\oplus}$)')
ax.set_title('Distribución Masa-Distancia')
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig('Distribucion_Masa_Distancia.png', dpi=300, bbox_inches='tight')
plt.show()

# --- PRUEBA 2: EXCENTRICIDAD VS DISTANCIA CON ERRORES ---
plt.figure(figsize=(12, 8))

e_err = [np.abs(df_err['pl_orbeccenerr2']), df_err['pl_orbeccenerr1']]

plt.errorbar(df_err['pl_orbsmax'], df_err['pl_orbeccen'], 
             xerr=x_err, yerr=e_err,
             fmt='o', markersize=2, color='darkorange', ecolor='gray', 
             elinewidth=0.3, capsize=0, alpha=0.3)

plt.axvline(0.1, color='red', linestyle='--', label='Límite de Marea')
plt.xscale('log')
plt.xlabel('Semieje Mayor $a$ (UA)')
plt.ylabel('Excentricidad $e$')
plt.ylim(-0.05, 1.0)
plt.title('Excentricidad y Distancia (Prueba con Errores)')
plt.savefig('Prueba_Excentricidad_Errores.png', dpi=300)
plt.show()














