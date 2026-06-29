# -*- coding: utf-8 -*-
"""
Calcular límites de la Zona Habitable, según Kopparapu, 
devolviendo como resultado una tabla.
"""

import numpy as np
import pandas as pd

def calcular_zh(L_estrella, T_eff):
    """
    Calcula los límites de la Zona Habitable (Kopparapu et al. 2013).
    L_estrella: Luminosidad en unidades solares (L_sun)
    T_eff: Temperatura efectiva en Kelvin (K)
    """
    # Coeficientes de Kopparapu para una Tierra (Standard)
    # [Runaway Greenhouse, Maximum Greenhouse]
    S_eff_sun = [1.107, 0.356]
    a = [1.332e-4, 6.171e-5]
    b = [1.58e-8, 1.698e-9]
    
    t_star = T_eff - 5780
    
    limites_UA = []
    for i in range(2):
        # Cálculo del flujo estelar efectivo (Seff)
        seff = S_eff_sun[i] + a[i]*t_star + b[i]*t_star**2
        # Conversión de flujo a distancia en Unidades Astronómicas (UA)
        distancia = np.sqrt(L_estrella / seff)
        limites_UA.append(round(distancia, 4))
        
    return limites_UA

# --- CASOS DE ESTUDIO ---
estrellas = {
    "Sol": {"L": 1.0, "T": 5780},
    "Proxima Centauri": {"L": 0.0017, "T": 3042},
    "TRAPPIST-1": {"L": 0.00055, "T": 2566}
}

print(f"{'Estrella':<20} | {'Límite Int (UA)':<15} | {'Límite Ext (UA)':<15}")
print("-" * 55)

for nombre, datos in estrellas.items():
    li, le = calcular_zh(datos["L"], datos["T"])











    print(f"{nombre:<20} | {li:<15} | {le:<15}")
