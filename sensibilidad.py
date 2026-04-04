import numpy as np
import numpy_financial as npf

# -----------------------------
# SENSIBILIDAD VPN VS TASA
# -----------------------------
def sensibilidad_vpn(flujos, min_tasa=0.01, max_tasa=0.5, pasos=30):
    tasas = np.linspace(min_tasa, max_tasa, pasos)
    vpns = [npf.npv(t, flujos) for t in tasas]
    return tasas * 100, vpns

# -----------------------------
# PUNTO CRÍTICO (VPN = 0)
# -----------------------------
def punto_equilibrio_tasa(flujos):
    tasas = np.linspace(0.01, 1, 100)
    for t in tasas:
        vpn = npf.npv(t, flujos)
        if abs(vpn) < 1000:
            return t * 100
    return None