# -*- coding: utf-8 -*-
"""
Análisis del Valle de Radio (Radius Valley) - Muestra Gaia Tipo G
Filtros de alta precisión para eliminar el ruido observacional.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Carga de datos
plt.close('all')
df = pd.read_csv('planetas.csv', comment='#')

# --- 2. FILTRADO DE ALTA CALIDAD (LA CLAVE DEL ÉXITO) ---

# A. Filtro por tipo espectral G (Análogos Solares según Gaia)
# Estrellas con temperatura efectiva entre 5200K y 6000K
df_g = df[(df['st_teff'] >= 5200) & (df['st_teff'] < 6000)].copy()

# B. Filtro de precisión de Radio (Gaia/Kepler Precision)
# Solo aceptamos planetas cuyo error en el radio sea inferior al 10% de su valor.
# Esto elimina los planetas con radios "borrosos" que tapan el valle.
df_g = df_g[df_g['pl_radeerr1'].notna()] # Eliminar NaNs primero
df_g = df_g[(df_g['pl_radeerr1'] / df_g['pl_rade']) <= 0.10]

# C. Filtro de Periodo Orbital
# El valle es más nítido en planetas cercanos donde la fotoevaporación actúa.
df_g = df_g[df_g['pl_orbper'] < 100]

# D. Limpieza final de valores nulos en el radio planetario
df_final = df_g[df_g['pl_rade'].notna()].copy()

# --- 3. CONFIGURACIÓN DEL HISTOGRAMA ---

plt.figure(figsize=(12, 7))
plt.style.use('seaborn-v0_8-whitegrid')

# Definimos los bins de forma fina (de 0.8 a 3.5 radios terrestres)
# Usar bins demasiado anchos puede ocultar el valle.
bins = np.linspace(0.8, 3.5, 35)

# Dibujamos el histograma con el filtro G de alta calidad
n, bins_h, patches = plt.hist(df_final['pl_rade'], bins=bins, 
                             color='lightblue', alpha=0.7, 
                             edgecolor='black', linewidth=1,
                             label=f'Muestra Tipo G Alta Precisión (N={len(df_final)})')

# --- 4. RESALTADO DEL VALLE DE RADIO ---

# Marcamos el gap teórico (Fulton et al. 2017)
plt.axvspan(1.51, 1.99, color='red', alpha=0.12, label='Radius Valley (Gap)')

# Líneas verticales para marcar los picos (opcional, ayuda a la vista)
# El primer pico (Super-Tierras) suele estar en ~1.3 Re
# El segundo pico (Mini-Neptunos) suele estar en ~2.4 Re
plt.axvline(1.3, color='darkgreen', linestyle='--', alpha=0.5)
plt.axvline(2.4, color='darkblue', linestyle='--', alpha=0.5)

# --- 5. ESTÉTICA PROFESIONAL ---

plt.title('Distribución Bimodal de Radios: Evidencia de Fotoevaporación', fontsize=15, fontweight='bold')
plt.xlabel(r'Radio Planetario ($R_{\oplus}$)', fontsize=13)
plt.ylabel('Número de Planetas', fontsize=13)
plt.xlim(0.8, 3.5)
plt.legend(frameon=True, fontsize=11)

# Guardar con alta resolución para el PDF de LaTeX
plt.savefig('Histograma_Radius_Valley_Final.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Planetas procesados con éxito: {len(df_final)}")






print(f"Planetas en la muestra final: {len(df_fgk)}")