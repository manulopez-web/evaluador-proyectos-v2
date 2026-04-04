import numpy_financial as npf
import numpy as np

# -----------------------------
# VPN
# -----------------------------
def calcular_vpn(tasa, flujos):
    return npf.npv(tasa, flujos)

# -----------------------------
# TIR
# -----------------------------
def calcular_tir(flujos):
    return npf.irr(flujos)

# -----------------------------
# PAYBACK SIMPLE
# -----------------------------
def calcular_payback(flujos):
    acumulado = 0
    for i, f in enumerate(flujos):
        acumulado += f
        if acumulado >= 0:
            return i
    return None

# -----------------------------
# PAYBACK DESCONTADO
# -----------------------------
def calcular_payback_descontado(tasa, flujos):
    acumulado = 0
    for i, f in enumerate(flujos):
        acumulado += f / ((1 + tasa) ** i)
        if acumulado >= 0:
            return i
    return None

# -----------------------------
# RBC (Relación Beneficio/Costo)
# -----------------------------
def calcular_rbc(tasa, flujos):
    beneficios = sum(f / ((1 + tasa) ** i) for i, f in enumerate(flujos) if f > 0)
    costos = abs(sum(f / ((1 + tasa) ** i) for i, f in enumerate(flujos) if f < 0))
    return beneficios / costos if costos != 0 else 0

# -----------------------------
# ÍNDICE DE RENTABILIDAD (PI)
# -----------------------------
def calcular_pi(tasa, flujos):
    inversion = abs(flujos[0])
    beneficios = sum(f / ((1 + tasa) ** i) for i, f in enumerate(flujos) if i != 0)
    return beneficios / inversion if inversion != 0 else 0

# -----------------------------
# FLUJO ACUMULADO
# -----------------------------
def flujo_acumulado(flujos):
    return np.cumsum(flujos)

# -----------------------------
# ESCENARIOS
# -----------------------------
def calcular_escenarios(vpn):
    return {
        "optimista": vpn * 1.2,
        "base": vpn,
        "pesimista": vpn * 0.8
    }

# -----------------------------
# RIESGO
# -----------------------------
def evaluar_riesgo(vpn_pesimista):
    return "Bajo" if vpn_pesimista > 0 else "Alto"

# -----------------------------
# SCORE COMBINADO (FINANCIERO + SOCIAL)
# -----------------------------
def calcular_score(vpn, impacto):
    return vpn + (impacto * 1_000_000)

# -----------------------------
# VALIDACIÓN DE DATOS
# -----------------------------
def validar_flujos(flujos):
    if len(flujos) < 2:
        return False
    if flujos[0] >= 0:
        return False
    return True