import pandas as pd

def exportar_excel_completo(df, nombre="resultado_proyectos.xlsx"):

    with pd.ExcelWriter(nombre, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Resumen", index=False)

        # hoja resumen ejecutivo
        resumen = pd.DataFrame({
            "Indicador": ["Mejor Proyecto", "VPN Máximo"],
            "Valor": [df.iloc[0]["Proyecto"], df["VPN"].max()]
        })

        resumen.to_excel(writer, sheet_name="Conclusión", index=False)

    return nombre