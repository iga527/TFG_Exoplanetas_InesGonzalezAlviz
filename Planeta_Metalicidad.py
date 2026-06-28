# -*- coding: utf-8 -*-
"""
Gráficas de Demografía Planetaria Independientes - TFG
Separación de Masa-Distancia y Excentricidad-Distancia
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Carga de datos
df = pd.read_csv('planetas.csv', comment='#')

# Limpieza básica
df = df[df['pl_orbsmax'] > 0] 

# Configuración de estilo global
plt.style.use('seaborn-v0_8-whitegrid')



# --- GRÁFICA 1: EXCENTRICIDAD VS SEMIEJE MAYOR ---
plt.figure(figsize=(10, 7))
df_ecc = df[df['pl_orbeccen'].notna()]
plt.scatter(df_ecc['pl_orbsmax'], df_ecc['pl_orbeccen'], alpha=0.4, s=16, color='darkorange', label='Exoplanetas')

# Línea de circularización por marea
plt.axvline(0.1, color='red', linestyle='--', alpha=0.6, label='Límite de Marea (0.1 UA)')

plt.xscale('log')
plt.xlabel('Semieje Mayor $a$ (UA)', fontsize=14)
plt.ylabel('Excentricidad $e$', fontsize=14)
plt.title('Excentricidad y Distancia Orbital', fontweight='bold', fontsize=14)
plt.ylim(-0.05, 1.2)
plt.legend(loc='upper right', fontsize=15)

plt.tight_layout()
plt.savefig('Excentricidad_Distancia.png', dpi=300)
plt.show()

# --- GRÁFICA 3: METALICIDAD VS GIGANTES (Histograma) ---
# (Se mantiene independiente como ya la tenías)
plt.figure(figsize=(10, 6))
gigantes = df[df['pl_bmasse'] > 100]['st_met'].dropna()
pequenos = df[df['pl_bmasse'] < 10]['st_met'].dropna()

plt.hist(gigantes, bins=30, alpha=0.5, density=True, label='Estrellas con Gigantes', color='crimson')
plt.hist(pequenos, bins=30, alpha=0.5, density=True, label='Estrellas con Planetas Pequeños', color='teal')

plt.xlabel('Metalicidad Estelar [Fe/H]', fontsize=14)
plt.ylabel('Densidad de Probabilidad', fontsize=14)
plt.title('Correlación Planeta-Metalicidad', fontweight='bold', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('Metalicidad_Correlacion.png', dpi=300)




















plt.show()