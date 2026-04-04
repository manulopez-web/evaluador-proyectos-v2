import streamlit as st
import pandas as pd
import numpy as np
from indicadores import *
from sensibilidad import *
from exportar import *

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Evaluador Proyectos PRO", layout="wide")

# -------------------------
# ESTILO PREMIUM
# -------------------------
st.markdown("""
<style>

/* Fuente */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Fondo elegante claro (NO oscuro total) */
.stApp {
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}

/* Títulos */
h1, h2, h3 {
    color: #1f2937;
    text-align: center;
}

/* Texto general */
p, label, div {
    color: #111827 !important;
}

/* Tarjetas KPI */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    text-align: center;
}

/* Botón */
.stButton>button {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

/* Tablas */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px;
    font-weight: bold;
    color: #1f2937;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("📊 Calculadora financiera de Evaluación de Proyectos")
st.markdown("### 🚀 Evaluador Inteligente de Proyectos")
st.caption("Análisis financiero, social y toma de decisiones en tiempo real")

modo = st.selectbox("Tipo de proyecto", ["Empresarial", "Social"])
num = st.number_input("Número de proyectos", min_value=1, value=1)

proyectos = []

# -------------------------
# INPUT
# -------------------------
for p in range(num):
    with st.expander(f"📁 Proyecto {p+1}", expanded=True):

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre del proyecto", key=f"n{p}")
            inversion = st.number_input("Inversión inicial", key=f"inv{p}")
            tasa = st.number_input("Tasa (%)", key=f"t{p}") / 100

        with col2:
            años = st.number_input("Años", min_value=1, key=f"a{p}")

        flujos = [-abs(inversion)]

        for i in range(1, años+1):
            flujo = st.number_input(f"Flujo año {i}", key=f"f{p}{i}")
            flujos.append(flujo)

        impacto = 0
        if modo == "Social":
            impacto = st.slider("Impacto social", 1, 5, 3)

        proyectos.append((nombre, tasa, flujos, impacto))

# -------------------------
# BOTÓN
# -------------------------
if st.button("🚀 ANALIZAR PROYECTOS"):

    resultados = []

    for nombre, tasa, flujos, impacto in proyectos:

        if not validar_flujos(flujos):
            st.error(f"Error en flujos del proyecto {nombre}")
            st.stop()

        vpn = calcular_vpn(tasa, flujos)
        tir = calcular_tir(flujos)
        payback = calcular_payback(flujos)
        pay_desc = calcular_payback_descontado(tasa, flujos)
        rbc = calcular_rbc(tasa, flujos)
        pi = calcular_pi(tasa, flujos)

        escenarios = calcular_escenarios(vpn)
        riesgo = evaluar_riesgo(escenarios["pesimista"])
        score = calcular_score(vpn, impacto)

        resultados.append({
            "Proyecto": nombre,
            "VPN": round(vpn, 2),
            "TIR (%)": round(tir * 100, 2),
            "Payback": payback,
            "Payback Desc": pay_desc,
            "RBC": round(rbc, 2),
            "PI": round(pi, 2),
            "Impacto": impacto,
            "Score": round(score, 2),
            "Riesgo": riesgo,
            "VPN Optimista": round(escenarios["optimista"], 2),
            "VPN Pesimista": round(escenarios["pesimista"], 2)
        })

    df = pd.DataFrame(resultados)

    if len(df) > 1:
        df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

    mejor = df.iloc[0]

    st.divider()
    st.subheader("🏆 Resumen Ejecutivo")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Proyecto", mejor["Proyecto"])
    col2.metric("VPN", mejor["VPN"])
    col3.metric("TIR (%)", mejor["TIR (%)"])
    col4.metric("Riesgo", mejor["Riesgo"])

    st.subheader("📊 Resultados")
    st.dataframe(df)

    # -------------------------
    # COMPARACIÓN
    # -------------------------
    if len(df) > 1:

        segundo = df.iloc[1]
        costo = mejor["VPN"] - segundo["VPN"]

        st.warning(f"⚠️ Costo de oportunidad: {round(costo,2)}")
        st.success(f"✔ Mejor alternativa: {mejor['Proyecto']}")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 VPN")
            st.bar_chart(df.set_index("Proyecto")["VPN"])

        with col2:
            st.subheader("📊 TIR (%)")
            st.bar_chart(df.set_index("Proyecto")["TIR (%)"])

    else:
        st.info("Análisis individual (no hay comparación entre proyectos)")

    # -------------------------
    # SENSIBILIDAD
    # -------------------------
    st.subheader("📉 Sensibilidad del VPN")

    tasas, vpns = sensibilidad_vpn(flujos)
    sens_df = pd.DataFrame({"Tasa": tasas, "VPN": vpns})

    st.line_chart(sens_df.set_index("Tasa"))

    punto = punto_equilibrio_tasa(flujos)

    if punto:
        st.info(f"El proyecto deja de ser viable cerca de una tasa del {round(punto,2)}%")

    # -------------------------
    # ESCENARIOS
    # -------------------------
    st.subheader("📊 Escenarios")

    esc_df = df[["Proyecto", "VPN Optimista", "VPN", "VPN Pesimista"]]
    st.dataframe(esc_df)

    # -------------------------
    # EXPORTAR
    # -------------------------
    archivo = exportar_excel_completo(df)

    with open(archivo, "rb") as f:
        st.download_button("📥 Descargar reporte en Excel", f, file_name=archivo)

    # -------------------------
    # CONCLUSIÓN
    # -------------------------
    st.subheader("🧠 Conclusión Inteligente")

    if len(df) == 1:

        if mejor["VPN"] > 0:
            st.success(f"""
            El proyecto **{mejor['Proyecto']}** es viable financieramente.

            Genera valor y puede ejecutarse bajo condiciones actuales.
            """)

        else:
            if modo == "Social":
                st.warning(f"""
                El proyecto **{mejor['Proyecto']}** no es rentable financieramente.

                Sin embargo, tiene un impacto social de {mejor['Impacto']}/5,
                por lo que puede justificarse desde una perspectiva social.
                """)
            else:
                st.error(f"""
                El proyecto **{mejor['Proyecto']}** no es viable financieramente.

                Presenta pérdida de valor (VPN negativo).
                """)

    else:

        if mejor["VPN"] > 0:
            st.success(f"""
            El proyecto **{mejor['Proyecto']}** es la mejor opción disponible.

            Presenta mayor generación de valor y mejor rentabilidad.
            """)

        else:
            st.warning(f"""
            Ninguno de los proyectos es viable financieramente.

            El menos desfavorable es **{mejor['Proyecto']}**.
            """)