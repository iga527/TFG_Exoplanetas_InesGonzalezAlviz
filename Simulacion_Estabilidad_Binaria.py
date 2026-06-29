# -*- coding: utf-8 -*-
"""
Simulacion del Problema Restringido de Tres Cuerpos (PR3C) 
Estabilidad orbital en sistemas binarios.

"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. LIMPIEZA Y CONFIGURACION DE CARPETA
# ============================================================
plt.close('all')
try:
    ruta = os.path.dirname(os.path.abspath(__file__))
    os.chdir(ruta)
except Exception:
    pass

# ============================================================
# 2. PARAMETROS FISICOS (unidades adimensionales: G=1, M1+M2=1, a_bin=1)
# ============================================================
mu = 0.3        # Relacion de masas M2 / (M1 + M2)
x1 = -mu        # Posicion Estrella 1
x2 = 1 - mu     # Posicion Estrella 2


def aceleracion(state):
    """Ecuaciones del movimiento en el sistema rotante (PR3C)."""
    x, y, vx, vy = state
    r1 = np.sqrt((x - x1)**2 + y**2)
    r2 = np.sqrt((x - x2)**2 + y**2)

    # Ecuaciones de movimiento incluyendo fuerzas de Coriolis y centrifuga
    ax = 2*vy + x - (1 - mu)*(x - x1)/r1**3 - mu*(x - x2)/r2**3
    ay = -2*vx + y - (1 - mu)*y/r1**3 - mu*y/r2**3
    return np.array([vx, vy, ax, ay])


def rk4_step(state, dt):
    """Integrador Runge-Kutta de 4º orden, paso fijo."""
    k1 = aceleracion(state)
    k2 = aceleracion(state + k1 * dt / 2)
    k3 = aceleracion(state + k2 * dt / 2)
    k4 = aceleracion(state + k3 * dt)
    return state + (dt / 6) * (k1 + 2*k2 + 2*k3 + k4)


def jacobi(state):
    """
    Constante de Jacobi del PR3C circular. Es una cantidad exactamente
    conservada por la dinamica real, por lo que sirve como prueba
    independiente de la fiabilidad numerica de la integracion: si C
    no se conserva, el problema es del integrador, no de la fisica.
    """
    x, y, vx, vy = state
    r1 = np.sqrt((x - x1)**2 + y**2)
    r2 = np.sqrt((x - x2)**2 + y**2)
    return x**2 + y**2 + 2*(1 - mu)/r1 + 2*mu/r2 - (vx**2 + vy**2)


# ============================================================
# 3. CONDICIONES INICIALES
# ============================================================

# --- 3.1 Orbita estable (tipo P, circumbinaria) -----------------------------
# v_y = -3.0 es, aproximadamente, la velocidad de una orbita ligada a
# r0 = 3.5 en el marco rotante (se determino comprobando numericamente
# que mantiene el radio acotado, sin necesidad de recortar los ejes).
dt_estable = 0.01
pasos_estable = 15000
s_estable = np.array([3.5, 0.0, 0.0, -3.0])

# --- 3.2 Trayectoria caotica (cerca del limite de Holman-Wiegert) ----------
# Paso temporal mas fino, porque esta trayectoria pasa mucho mas cerca
# de las estrellas que la orbita estable y los gradientes de fuerza
# son mayores ahi.
dt_caos = 0.005
pasos_caos = 7000
s_caos = np.array([1.9, 0.0, 0.0, -1.6])

# ============================================================
# 4. INTEGRACION
# ============================================================
hist_est, hist_caos = [], []

s = s_estable.copy()
for _ in range(pasos_estable):
    hist_est.append(s[:2].copy())
    s = rk4_step(s, dt_estable)
h_est = np.array(hist_est)

s = s_caos.copy()
for _ in range(pasos_caos):
    hist_caos.append(s[:2].copy())
    s = rk4_step(s, dt_caos)
h_caos = np.array(hist_caos)

# ============================================================
# 5. VALIDACION FISICA: CONSERVACION DE LA CONSTANTE DE JACOBI
# ============================================================
s_chk = s_estable.copy()
for _ in range(pasos_estable):
    s_chk = rk4_step(s_chk, dt_estable)
deriva_estable = abs(jacobi(s_chk) - jacobi(s_estable)) / abs(jacobi(s_estable)) * 100

s_chk = s_caos.copy()
for _ in range(pasos_caos):
    s_chk = rk4_step(s_chk, dt_caos)
deriva_caos = abs(jacobi(s_chk) - jacobi(s_caos)) / abs(jacobi(s_caos)) * 100

r_est = np.hypot(h_est[:, 0], h_est[:, 1])
print(f"Orbita estable : r_min={r_est.min():.3f}  r_max={r_est.max():.3f}  "
      f"deriva de C = {deriva_estable:.4f} %")
print(f"Trayectoria caotica : deriva de C = {deriva_caos:.4f} %")

# ============================================================
# 6. VISUALIZACION
# ============================================================
plt.figure(figsize=(10, 10))
plt.style.use('seaborn-v0_8-whitegrid')

# Estrellas
plt.plot(x1, 0, 'ro', markersize=12, label='Estrella 1 ($M_1$)')
plt.plot(x2, 0, 'bo', markersize=8, label='Estrella 2 ($M_2$)')

# Trayectorias
plt.plot(h_est[:, 0], h_est[:, 1], 'g-', alpha=0.7, lw=1.5,
          label='Órbita Estable (Tipo P)')
plt.plot(h_caos[:, 0], h_caos[:, 1], 'orange', alpha=0.8, lw=1.2,
          label='Trayectoria Caótica (Eyección)')

plt.xlim(-8, 8)
plt.ylim(-8, 8)
plt.title('Simulación Numérica RK4: Estabilidad en Sistemas Binarios',
           fontsize=14, fontweight='bold')
plt.xlabel('x (unidades de separación binaria $a$)', fontsize=12)
plt.ylabel('y (unidades de separación binaria $a$)', fontsize=12)
plt.legend(loc='upper right', frameon=True)
plt.gca().set_aspect('equal')
plt.grid(True, alpha=0.3)

plt.savefig('Simulacion_Estabilidad_Final.png', dpi=300, bbox_inches='tight')
plt.show()
print("Simulación terminada. Imagen guardada como 'Simulacion_Estabilidad_Final.png'")
