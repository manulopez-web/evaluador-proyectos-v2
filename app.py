import streamlit as st
import pandas as pd
from indicadores import *
from sensibilidad import *

st.title("💼 Sistema de Evaluación de Proyectos")

num = st.number_input("Número de proyectos", min_value=1, value=1)

resultados = []

for p in range(num):
    st.subheader(f"Proyecto {p+1}")
    
    nombre = st.text_input(f"Nombre del proyecto {p+1}", key=f"n{p}")
    inversion = st.number_input(f"Inversión inicial {p+1}", key=f"i{p}")
    tasa = st.number_input(f"Tasa de descuento (%) {p+1}", key=f"t{p}") / 100
    años = st.number_input(f"Años {p+1}", min_value=1, key=f"a{p}")

    flujos = [-abs(inversion)]

    for i in range(1, años+1):
        flujo = st.number_input(f"Flujo año {i} - Proyecto {p+1}", key=f"f{p}{i}")
        flujos.append(flujo)

    if st.button(f"Calcular Proyecto {p+1}", key=f"b{p}"):

        vpn = calcular_vpn(tasa, flujos)
        tir = calcular_tir(flujos)

        resultados.append({
            "Proyecto": nombre,
            "VPN": round(vpn, 2),
            "TIR": round(tir, 4)
        })
# -----------------------------
# RESULTADOS
# -----------------------------

if len(resultados) > 0:

    df = pd.DataFrame(resultados)
    df = df.sort_values(by="VPN", ascending=False)

    st.subheader("📊 Resultados")
    st.dataframe(df)

    # -----------------------------
    # EXPLICACIÓN SCORE
    # -----------------------------

    st.subheader("🧮 ¿Cómo se calcula el Score?")

    st.info("""
    El score es un indicador compuesto que combina:

    • El Valor Presente Neto (VPN)  
    • El impacto social del proyecto  

    Fórmula utilizada:

    Score = VPN + (Impacto social × 1,000,000)

    Esto permite priorizar proyectos que no solo sean rentables,
    sino que también generen valor social.
    """)

    # -----------------------------
    # MEJOR PROYECTO
    # -----------------------------

    mejor = df.iloc[0]

    st.success(f"🏆 Mejor proyecto: {mejor['Proyecto']}")

    # costo oportunidad SOLO si hay varios
    if len(df) > 1:

        segundo = df.iloc[1]
        costo = mejor["VPN"] - segundo["VPN"]

        st.warning(f"⚠️ Costo de oportunidad: {round(costo,2)}")

        st.info("""
        El costo de oportunidad representa la diferencia entre elegir
        la mejor alternativa frente a la segunda mejor opción disponible.
        """)

    else:

        st.info("""
        Solo se evaluó un proyecto, por lo tanto no se realiza comparación
        entre alternativas.
        """)

    # -----------------------------
    # GRÁFICO VPN
    # -----------------------------

    st.subheader("📈 Comparación de VPN")

    st.bar_chart(df.set_index("Proyecto")["VPN"])

    st.caption("Eje X: Proyectos evaluados | Eje Y: Valor Presente Neto (VPN)")

    # -----------------------------
    # SENSIBILIDAD
    # -----------------------------

    tasas, vpns = sensibilidad_vpn(flujos)

    st.subheader("📉 Sensibilidad del VPN")

    sens_df = pd.DataFrame({
        "Tasa (%)": tasas,
        "VPN": vpns
    })

    st.line_chart(sens_df.set_index("Tasa (%)"))

    st.caption("Eje X: Tasa de descuento (%) | Eje Y: Valor Presente Neto (VPN)")

    st.info("""
    El análisis de sensibilidad permite observar cómo cambia el VPN
    cuando se modifica la tasa de descuento.

    A medida que aumenta la tasa, el VPN tiende a disminuir,
    debido a que los flujos futuros pierden valor en el tiempo.
    """)

    # -----------------------------
    # ESCENARIOS
    # -----------------------------

    st.subheader("📊 Escenarios del Proyecto")

    st.write("""
    Se evaluaron tres escenarios:

    • Escenario actual: basado en los flujos ingresados  
    • Escenario optimista: incremento del 20% en el VPN  
    • Escenario pesimista: reducción del 20% en el VPN  

    Esto permite analizar la estabilidad del proyecto ante
    posibles cambios económicos o financieros.
    """)

    escenarios_df = pd.DataFrame({
        "Escenario": ["Pesimista", "Actual", "Optimista"],
        "VPN": [
            round(mejor["VPN"] * 0.8, 2),
            round(mejor["VPN"], 2),
            round(mejor["VPN"] * 1.2, 2)
        ]
    })

    st.dataframe(escenarios_df)

    st.bar_chart(escenarios_df.set_index("Escenario"))

    st.caption("Eje X: Escenarios | Eje Y: VPN")

    # -----------------------------
    # SUSTENTO DEL ANÁLISIS
    # -----------------------------

    st.subheader("📚 Sustento del análisis")

    st.write("""
    El análisis realizado se fundamenta en herramientas clásicas
    de evaluación financiera ampliamente utilizadas en la formulación
    y evaluación de proyectos.

    • VPN: mide la generación de valor  
    • TIR: mide la rentabilidad esperada  
    • Payback: mide el tiempo de recuperación  
    • RBC: compara beneficios frente a costos  

    En proyectos sociales, adicionalmente se incorpora
    el impacto social para complementar el análisis financiero.
    """)

    # -----------------------------
    # CONCLUSIÓN
    # -----------------------------

    st.subheader("🧠 Conclusión inteligente")

    if mejor["VPN"] > 0:

        st.success(f"""
        El proyecto {mejor['Proyecto']} presenta viabilidad financiera,
        debido a que genera valor económico positivo.

        Además, muestra estabilidad aceptable según el análisis
        de sensibilidad y escenarios.
        """)

    else:

        st.error(f"""
        El proyecto {mejor['Proyecto']} no presenta viabilidad financiera
        bajo las condiciones actuales, debido a un VPN negativo.

        Sin embargo, en proyectos sociales podría justificarse
        dependiendo del impacto social generado.
        """)