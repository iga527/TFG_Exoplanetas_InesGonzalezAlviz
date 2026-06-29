# -*- coding: utf-8 -*-
"""
Comparacion entre velocidad radial (1D) y astrometria (2D).
La velocidad radial y la astrometria no son dos fenomenos
fisicos distintos, sino dos proyecciones distintas del mismo movimiento
baricentrico de la estrella.

"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. PARAMETROS ORBITALES
# ============================================================

EXCENTRICIDAD = 0.35           # e
ARGUMENTO_PERIASTRO_DEG = 60    # omega (grados)
INCLINACION_DEG = 50            # i (grados)
SEMIAMPLITUD_K = 1.0             # K, normalizada a 1 (unidades arbitrarias)
N_EPOCAS = 6                     # numero de instantes marcados en ambos paneles

omega = np.radians(ARGUMENTO_PERIASTRO_DEG)
i_rad = np.radians(INCLINACION_DEG)

plt.rcParams.update({
    "font.family":        "serif",
    "mathtext.fontset":   "stix",
    "font.size":          13,
    "axes.labelsize":     14,
    "xtick.labelsize":    12,
    "ytick.labelsize":    12,
    "axes.titlesize":     14,
    "figure.titlesize":   13,

})


# ============================================================
# 2. ECUACION DE KEPLER
# ============================================================
def resolver_kepler(M, e, n_iter=80):
    """
    Resuelve la ecuacion de Kepler M = E - e sin(E) para la anomalia
    excentrica E, dada la anomalia media M, mediante iteracion de
    Newton-Raphson.
    """
    E = M.copy()
    for _ in range(n_iter):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def anomalia_verdadera(E, e):
    """Convierte la anomalia excentrica E en anomalia verdadera nu."""
    return 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                           np.sqrt(1 - e) * np.cos(E / 2))


# ============================================================
# 3. POSICION ORBITAL Y PROYECCION SOBRE EL PLANO DEL CIELO
# ============================================================
def posicion_en_plano_del_cielo(nu, E, e, omega, i_rad):
    """
    A partir de la anomalia verdadera nu y excentrica E, devuelve la
    posicion proyectada (X, Y) sobre el plano del cielo.

    Paso 1: posicion en el plano orbital, con el periastro a lo largo
            del eje x' (forma focal: r = a(1 - e cos E), con el foco
            -es decir, el baricentro- en el origen).
    Paso 2: rotacion en el plano orbital por el argumento del
            periastro omega.
    Paso 3: inclinacion del plano orbital un angulo i alrededor del
            eje x (linea de nodos). La componente Y se acorta por un
            factor cos(i); la componente perdida pasa al eje z
            (linea de vision), de donde proviene la velocidad radial.
    """
    r = 1 - e * np.cos(E)
    x_orb = r * np.cos(nu)
    y_orb = r * np.sin(nu)

    x1 = x_orb * np.cos(omega) - y_orb * np.sin(omega)
    y1 = x_orb * np.sin(omega) + y_orb * np.cos(omega)

    X = x1
    Y = y1 * np.cos(i_rad)
    return X, Y


def velocidad_radial(nu, e, omega, K):
    """
    Velocidad radial analitica (ecuacion 2.7 del TFG):

        v_r(t) = K [cos(omega + nu(t)) + e cos(omega)]
    """
    return K * (np.cos(omega + nu) + e * np.cos(omega))


# ============================================================
# 4. CURVAS COMPLETAS (para trazar las lineas continuas)
# ============================================================
n_puntos = 400
M = np.linspace(0, 2 * np.pi, n_puntos)
E = resolver_kepler(M, EXCENTRICIDAD)
nu = anomalia_verdadera(E, EXCENTRICIDAD)

X, Y = posicion_en_plano_del_cielo(nu, E, EXCENTRICIDAD, omega, i_rad)
vr = velocidad_radial(nu, EXCENTRICIDAD, omega, SEMIAMPLITUD_K)
fase = M / (2 * np.pi)

# ============================================================
# 5. EPOCAS MARCADAS (puntos numerados, compartidos entre paneles)
# ============================================================
M_ep = np.linspace(0, 2 * np.pi, N_EPOCAS, endpoint=False)
E_ep = resolver_kepler(M_ep, EXCENTRICIDAD)
nu_ep = anomalia_verdadera(E_ep, EXCENTRICIDAD)

X_ep, Y_ep = posicion_en_plano_del_cielo(nu_ep, E_ep, EXCENTRICIDAD, omega, i_rad)
vr_ep = velocidad_radial(nu_ep, EXCENTRICIDAD, omega, SEMIAMPLITUD_K)
fase_ep = M_ep / (2 * np.pi)


# ============================================================
# 6. FIGURA: DOS PANELES
# ============================================================
fig, (ax_rv, ax_astro) = plt.subplots(1, 2, figsize=(11.2, 4.7))

# --- 6.1 Panel A: velocidad radial (1D) ------------------------------------
ax_rv.plot(fase, vr, "k-", lw=1.7, zorder=3)
ax_rv.axhline(0, color="gray", ls="--", lw=0.9, zorder=1)

ax_rv.scatter(fase_ep, vr_ep, s=42, c="steelblue", zorder=5,
              edgecolor="k", linewidth=0.5)
for n, (xe, ye) in enumerate(zip(fase_ep, vr_ep), start=1):
    ax_rv.annotate(str(n), (xe, ye), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8.5)

ax_rv.set_xlabel("Fase orbital")
ax_rv.set_ylabel(r"Velocidad radial, $v_r$")
ax_rv.set_title("Velocidad radial — 1D", fontsize=12)
ax_rv.set_xlim(-0.02, 1.02)
ax_rv.spines["top"].set_visible(False)
ax_rv.spines["right"].set_visible(False)

# --- 6.2 Panel B: astrometria (2D) ------------------------------------------
ax_astro.plot(X, Y, "k-", lw=1.7, zorder=3)
ax_astro.scatter([0], [0], marker="+", s=70, c="k", zorder=4)
ax_astro.text(0.05, -0.18, "Baricentro", fontsize=8, color="gray")

ax_astro.scatter(X_ep, Y_ep, s=42, c="steelblue", zorder=5,
                  edgecolor="k", linewidth=0.5)
for n, (xe, ye) in enumerate(zip(X_ep, Y_ep), start=1):
    ax_astro.annotate(str(n), (xe, ye), textcoords="offset points",
                       xytext=(7, 7), ha="center", fontsize=8.5)

ax_astro.set_xlabel(r"$\Delta\alpha\cos\delta$")
ax_astro.set_ylabel(r"$\Delta\delta$")
ax_astro.set_title("Astrometría — 2D", fontsize=12)
ax_astro.set_aspect("equal")
ax_astro.spines["top"].set_visible(False)
ax_astro.spines["right"].set_visible(False)
ax_astro.invert_xaxis()  # convencion astronomica: ascension recta creciente hacia la izquierda

fig.suptitle("Mismo movimiento baricéntrico, dos proyecciones complementarias",
             fontsize=11.5, y=1.02, style="italic")

plt.tight_layout()

# ============================================================
# 7. EXPORTACION
# ============================================================
plt.savefig("comparacion_rv_astrometria.png", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.savefig("comparacion_rv_astrometria.pdf", dpi=200,
            bbox_inches="tight", facecolor="white")
plt.show()
