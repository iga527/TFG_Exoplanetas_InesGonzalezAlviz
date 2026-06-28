# -*- coding: utf-8 -*-
"""
Simulacion de espectros de transmision: atmosfera primordial de H/He
(con trazas de H2O) frente a atmosfera secundaria de CO2.

"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Configuracion inicial
plt.close('all')
np.random.seed(42)   # fija el ruido para que la figura sea reproducible

# 2. Definicion del espectro (longitudes de onda de 1 a 5 micras, rango JWST)
wavelengths = np.linspace(1.0, 5.0, 500)

# --- Calculo trazable de las alturas de pico para la atmosfera de H/He ---
razon_mu = 44.0 / 2.3                 # mu(CO2) / mu(H/He)
ref_co2 = 100                          # ppm: banda de CO2 a 2.0 um (sin anomalia de seccion eficaz)
ref_hhe = ref_co2 * razon_mu           # ppm: senal equivalente para mu=2.3

# Proporciones relativas originales de las bandas de H2O, normalizadas a su banda mas fuerte
proporciones_h2o = {'1.4': 200/450, '1.9': 350/450, '2.7': 1.0}
alturas_h2o_hhe = {k: ref_hhe * v for k, v in proporciones_h2o.items()}
# {'1.4': ~850, '1.9': ~1488, '2.7': ~1913} ppm


def simular_absorcion(wl, escenario):
    """
    escenario: 'HHe_H2O'   -> atmosfera primordial de H/He, trazas de H2O
               'CO2'        -> atmosfera secundaria de CO2
    """
    base = 1500  # ppm, profundidad de transito continua (misma referencia en ambos casos)

    if escenario == 'HHe_H2O':
        peaks = [1.4, 1.9, 2.7]
        widths = [0.1, 0.15, 0.2]
        heights = [alturas_h2o_hhe['1.4'], alturas_h2o_hhe['1.9'], alturas_h2o_hhe['2.7']]
    else:  # CO2
        peaks = [2.0, 2.7, 4.3]
        widths = [0.1, 0.2, 0.35]
        heights = [100, 300, 800]   # sin cambios: 4.3 um sigue dominado por su seccion eficaz

    spectrum = np.full_like(wl, base)
    for p, w, h in zip(peaks, widths, heights):
        spectrum += h * np.exp(-0.5 * ((wl - p) / w) ** 2)

    # Ruido gaussiano (precision fotonica del instrumento), semilla fija.
    # sigma=40 ppm, dentro del rango 10-50 ppm que el texto del capitulo
    # ya justifica como umbral practico de deteccion.
    noise = np.random.normal(0, 40, len(wl))
    return spectrum + noise


# 3. Generar datos
spec_hhe = simular_absorcion(wavelengths, 'HHe_H2O')
spec_co2 = simular_absorcion(wavelengths, 'CO2')

# 4. Grafico
plt.figure(figsize=(12, 6))
plt.style.use('seaborn-v0_8-whitegrid')
plt.plot(wavelengths, spec_hhe, color='royalblue', alpha=0.8,
          label=r'Atmósfera primordial H/He ($\mu \approx 2{,}3$ u), trazas de $H_2O$')
plt.plot(wavelengths, spec_co2, color='crimson', alpha=0.8,
          label=r'Atmósfera secundaria de $CO_2$ ($\mu \approx 44$ u)')

plt.title('Simulación de Espectros de Transmisión (Sensibilidad JWST/NIRSpec)',
           fontsize=14, fontweight='bold')
plt.xlabel(r'Longitud de onda ($\mu m$)', fontsize=12)
plt.ylabel('Profundidad del Tránsito (ppm)', fontsize=12)
plt.legend(loc='upper left', frameon=True, fontsize=9.5)
plt.ylim(1300, 3600)

plt.savefig('Simulacion_Espectros_Atmosfericos.png', dpi=300, bbox_inches='tight')
plt.show()









print("Alturas H/He (ppm):", {k: round(v) for k, v in alturas_h2o_hhe.items()})