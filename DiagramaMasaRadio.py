# -*- coding: utf-8 -*-
"""
Diagrama Masa-Radio Final - TFG
Version corregida: cobertura completa de datos y curvas teoricas
restringidas a su rango de validez fisica.

Que cambia respecto a la version anterior
-------------------------------------------
1. Las curvas de composicion pura (hierro, terrestre, agua/hielo) se
   generaban con el mismo exponente fijo (M^0.27) hasta M=10 000 M_tierra.
   El propio Capitulo 3 explica que esa ecuacion de estado "no describe
   adecuadamente las envolturas gaseosas de H/He presentes en gigantes
   gaseosos": las curvas se han limitado a M <= 200 M_tierra, justo donde
   el texto situa la transicion de Chen & Kipping al regimen de gigantes
   gaseosos. Comparar contra hierro o agua puros mas alla de ese punto
   no tiene sentido fisico, y los datos reales lo confirman: la mediana
   de radio observada apenas cambia entre 1000 y 9600 M_tierra (firma de
   la presion de degeneracion electronica), mientras que las curvas
   originales seguian creciendo sin limite.

2. La clasificacion de los datos por calidad (Grupo A: masa medida;
   Grupo B: Msini; Grupo C: radio imputado) dejaba fuera, sin avisar,
   cualquier planeta cuyo campo "pl_bmassprov" no fuera exactamente
   'Mass' o 'Msini'. En el catalogo real existe una tercera categoria,
   'M-R relationship' (masa estimada a partir del radio, no medida),
   que no encajaba en ningun grupo. Esto eliminaba 2713 de 6160 filas
   (un 44% de la muestra), incluyendo planetas con RADIO medido. Se
   anade un cuarto grupo, "Radio medido, masa imputada", que recoge
   exactamente esos casos. Los cuatro grupos juntos vuelven a sumar
   el total de filas del catalogo.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D

# 1. Configuracion y Carga
plt.close('all')
df = pd.read_csv('planetas.csv', comment='#')

# --- 2. CLASIFICACION DE DATOS ---

# Particion primaria: ¿el radio fue medido o imputado?
con_radio_medido = df['pl_radeerr1'].notna()

# Grupo A: radio medido + masa medida directamente, con error conocido
calidad_mask = con_radio_medido & (df['pl_bmassprov'] == 'Mass') & df['pl_bmasseerr1'].notna()
df_calidad = df[calidad_mask].copy()

# Grupo B: radio medido + masa minima (Msini), con error conocido
msini_mask = con_radio_medido & (df['pl_bmassprov'] == 'Msini') & df['pl_bmasseerr1'].notna()
df_msini = df[msini_mask].copy()

# Grupo C (NUEVO): radio medido, pero la masa no tiene barra de error
# fiable (con frecuencia porque la propia masa procede de una relacion
# masa-radio en vez de una medida independiente). Antes este grupo
# desaparecia del grafico sin dejar rastro.
otros_mask = con_radio_medido & ~calidad_mask & ~msini_mask
df_otros = df[otros_mask].copy()

# Grupo D: radio no medido, imputado por el catalogo (el "codo" teorico)
imputados_mask = ~con_radio_medido
df_imputados = df[imputados_mask].copy()

assert calidad_mask.sum() + msini_mask.sum() + otros_mask.sum() + imputados_mask.sum() == len(df), \
    "Los grupos no cubren el total de filas: revisar la logica de clasificacion."

# --- 3. CREACION DEL GRAFICO ---
fig, ax = plt.subplots(figsize=(14, 9))
plt.style.use('seaborn-v0_8-whitegrid')

# Funcion auxiliar para pintar con barras de error
def plot_with_errors(axis, dataframe, color, label, alpha_point=0.6):
    x_err = [np.abs(dataframe['pl_bmasseerr2']), dataframe['pl_bmasseerr1']]
    y_err = [np.abs(dataframe['pl_radeerr2']), dataframe['pl_radeerr1']]

    axis.errorbar(dataframe['pl_bmasse'], dataframe['pl_rade'],
                  xerr=x_err, yerr=y_err,
                  fmt='o', markersize=3, color=color, ecolor=color,
                  elinewidth=0.5, capsize=0, alpha=alpha_point, label=label,
                  markeredgecolor='none')

# Dibujamos los grupos con errores
plot_with_errors(ax, df_calidad, 'lightblue', 'Masa ($M$) y Radio medidos')
plot_with_errors(ax, df_msini, 'red', r'Masa mínima ($M \cdot \sin i$)')

# NUEVO: radio medido pero masa imputada o sin incertidumbre reportada.
# Sin barras de error en X (no son fiables para este grupo), pero SI
# se muestran, en vez de desaparecer del grafico. Color claramente
# distinto del gris de "imputados" para que no se confundan a simple
# vista (antes ambos grupos usaban tonos grisaceos casi identicos).
ax.scatter(df_otros['pl_bmasse'], df_otros['pl_rade'],
           color='mediumorchid', alpha=0.35, s=6,
           label='Radio medido, masa imputada', zorder=2)

# Dibujamos los imputados (muy tenues)
ax.scatter(df_imputados['pl_bmasse'], df_imputados['pl_rade'],
           color='darkgray', alpha=0.1, s=5, label='Radios estimados (Imputados)', zorder=1)

# --- 4. MODELOS TEORICOS ---
# Restringidos a M <= 200 M_tierra: mas alla de ese punto la ecuacion
# de estado de materiales condensados ya no describe la composicion
# dominante (envolturas de H/He), como se discute en el Capitulo 3.
M_MAX_TEORICA = 200
m_teorica = np.logspace(-1.2, np.log10(M_MAX_TEORICA), 500)
ax.plot(m_teorica, 0.70 * (m_teorica**0.27), '--', color='darkorange', alpha=0.8, label='100% Hierro', zorder=10)
ax.plot(m_teorica, 1.00 * (m_teorica**0.27), '-', color='saddlebrown', lw=2, label='Comp. Terrestre', zorder=11)
ax.plot(m_teorica, 1.25 * (m_teorica**0.27), '--', color='darkblue', alpha=0.8, label='100% Agua/Hielo', zorder=12)

# --- 5. ESTETICA Y LIMITES ---
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'Masa ($M_{\oplus}$)', fontsize=12)
ax.set_ylabel(r'Radio ($R_{\oplus}$)', fontsize=12)
ax.set_title('Diagrama Masa-Radio con Barras de Error e Incertidumbre', fontweight='bold', fontsize=14)

ax.set_xlim(0.07, 15000)
ax.set_ylim(0.4, 35)

# --- 6. SISTEMA SOLAR ---
ss_planets = {
    'Tierra': [1.0, 1.0],
    'Venus': [0.815, 0.949],
    'Marte': [0.107, 0.533],
    'Neptuno': [17.14, 3.88],
    'Urano': [14.53, 4.01],
    'Júpiter': [317.8, 11.2],
    'Saturno': [95.16, 9.45]
}

text_offsets = {
    'Tierra': (1.2, 0.95),
    'Venus': (1.2, 0.85),
    'Marte': (1.1, 0.9),
    'Neptuno': (1.2, 0.9),
    'Urano': (0.7, 1.1),
    'Júpiter': (1.2, 1.0),
    'Saturno': (1.2, 0.9)
}

for nombre, datos in ss_planets.items():
    ax.scatter(datos[0], datos[1], marker='X', color='red', s=120,
               zorder=100, edgecolors='black', linewidth=1.0)

    ox, oy = text_offsets.get(nombre, (1.2, 1.0))

    txt = ax.text(datos[0]*ox, datos[1]*oy, nombre, fontsize=11, fontweight='bold',
                  color='black', zorder=101)
    txt.set_path_effects([patheffects.withStroke(linewidth=3, foreground="white")])

# --- 7. LEYENDA ---
legend_elements = ax.get_legend_handles_labels()[0]
ss_legend_handle = Line2D([0], [0], marker='X', color='black', markerfacecolor='red',
                          markersize=10, label='Sistema Solar', linewidth=0)
legend_elements.append(ss_legend_handle)

ax.legend(handles=legend_elements, loc='upper left', fontsize=9, frameon=True)

plt.savefig('Diagrama_MR_Final_TFG.png', dpi=300, bbox_inches='tight')
plt.show()
print("Figura guardada. Grupos: calidad=%d, msini=%d, otros=%d, imputados=%d (suma=%d, total=%d)" %
      (calidad_mask.sum(), msini_mask.sum(), otros_mask.sum(), imputados_mask.sum(),










       calidad_mask.sum()+msini_mask.sum()+otros_mask.sum()+imputados_mask.sum(), len(df)))