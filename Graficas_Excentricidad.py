# -*- coding: utf-8 -*-
"""
Distribución Masa-Distancia con barras de error.

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# ─── 1. ESTILO ───────────────────────────────────────────────────────────────

plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams.update({
    'font.family':      'serif',
    'font.size':        14,
    'axes.labelsize':   14,
    'axes.titlesize':   14,
    'xtick.labelsize':  14,
    'ytick.labelsize':  14,
    'legend.fontsize':  14,
})

# ─── 2. CARGA DE DATOS ───────────────────────────────────────────────────────

df = pd.read_csv('planetas.csv', comment='#')

# Filtrado: planetas con errores en masa y semieje mayor disponibles.
# No se filtra por excentricidad: no es necesario para este diagrama.
df_err = df[
    df['pl_bmasseerr1'].notna()
    & df['pl_orbsmaxerr1'].notna()
].copy()

# ─── 3. FIGURA ───────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 8))

# Barras de error asimétricas (err2 es negativo por convención → abs)
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

# ─── 4. REFERENCIAS DEL SISTEMA SOLAR ────────────────────────────────────────
# Se incluyen todos los planetas cuya masa cae dentro del rango del diagrama.
# Mercurio (0.055 M⊕) queda justo por debajo del límite inferior original
# de 0.1 M⊕; se extiende el eje para mostrarlo (véase ax.set_ylim más abajo).
#
# Masas en M⊕ y semiejes en UA (valores medios IAU).
# Nota: los xytext son estimaciones iniciales; ajustar visualmente si es
# necesario tras comprobar la densidad local del diagrama.

ss_annotations = {
    'Mercurio': {'xy': (0.387,  0.055),  'xytext': (0.20,  0.08)},
    'Venus':    {'xy': (0.723,  0.815),  'xytext': (0.35,  0.45)},
    'Tierra':   {'xy': (1.000,  1.000),  'xytext': (1.30,  1.00)},
    'Marte':    {'xy': (1.524,  0.107),  'xytext': (2.00,  0.1)},
    'Júpiter':  {'xy': (5.203,  317.8),  'xytext': (6.80,  300.0)},
    'Saturno':  {'xy': (9.537,  95.16),  'xytext': (12.00, 93.0)},
    'Urano':    {'xy': (19.19,  14.54),  'xytext': (12.30, 7.00)},
    'Neptuno':  {'xy': (30.07,  17.15),  'xytext': (40.00, 15.0)},
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

# ─── 5. ESCALA, ETIQUETAS Y LÍMITES ──────────────────────────────────────────

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Semieje Mayor $a$ (UA)')
ax.set_ylabel(r'Masa $M_p$ ($M_{\oplus}$)')
ax.set_title('Distribución Masa-Distancia')

# El límite inferior se extiende a 0.03 M⊕ para mostrar Mercurio (0.055 M⊕)
# con un pequeño margen. Si se prefiere omitir Mercurio, comentar esta línea
# y el eje se auto-escalará hasta ~ 0.1 M⊕.
ax.set_ylim(bottom=0.03)

ax.legend(loc='upper left')

# ─── 6. EXPORTACIÓN ──────────────────────────────────────────────────────────

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














