from fpdf import FPDF
import pandas as pd
from configuracion import ESTRUCTURA_SEMAFORO

CANTIDAD_RENGLONES = 1

def promedios_por_indicador(diagnostico):
    promedios_indicador = pd.DataFrame()
    for indicador, info_seccion in ESTRUCTURA_SEMAFORO.items():
        preguntas_por_indicador = info_seccion[CANTIDAD_RENGLONES]
        promedios = []
        for _, row in diagnostico.iterrows():
            suma_preguntas = sum([row[indicador + str(n)] for n in range(preguntas_por_indicador)])
            promedio = suma_preguntas / preguntas_por_indicador
            promedios.append(promedio)
        promedios_indicador = promedios_indicador.append({
            'indicador' : indicador,
            'rojo' : (len([True for pr in promedios if pr < 0.33]) / len(promedios) ) * 100,
            'amarillo' : (len([True for pr in promedios if (0.33 < pr < .66)]) / len(promedios) ) * 100,
            'verde' : (len([True for pr in promedios if pr > .66]) / len(promedios) ) * 100
        }, ignore_index=True)
        
    return promedios_indicador

def generar_reporte(diagnostico, directorio_resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)

    pdf.cell(60)
    id_facilitador = diagnostico['ID_Facilitador'].iloc[0]
    # TÍTULO
    pdf.cell(75, 10, f"Informe de Facilitador #{id_facilitador}", 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-40)
    
    #
    # INFO DEL FACILITADOR
    #
    pdf.set_font('Arial', 'B', 14)
    # Territorio
    pdf.cell(50, 10, 'Territorio', 1, 0, 'R')
    pdf.cell(40, 10, 'Pantano', 1, 2, 'C')
    pdf.cell(-50)
    # Año de aplicación:
    pdf.cell(50, 10, 'Año de aplicación:', 1, 0, 'R')
    pdf.cell(40, 10, '...FECHA...', 1, 2, 'C')
    pdf.cell(-50)
    # Iteración:
    pdf.cell(50, 10, 'Iteración', 1, 0, 'R')
    iteracion = diagnostico['Iteracion'].iloc[0]
    pdf.cell(40, 10, iteracion, 1, 2, 'C')
    pdf.cell(-50)
    # Gradiente social:	Rojo: si los indicadores en verde son menores que 33% y los rojos mayores que 33% | Verde: si los indicadores en rojo son menores que 25% y los indicadores verdes mayores que 40% | Amarillo: else			
    pdf.cell(50, 10, 'Gradiente Social:', 1, 0, 'R')
    pdf.cell(40, 10, '...GRADIENTE...', 1, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-60)
    

    # ENCABEZADOS INDICADORES
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 8, 'Indicador', 1, 0, 'L')
    pdf.cell(30, 8, 'Rojo', 1, 0, 'C')
    pdf.cell(30, 8, 'Amarillo', 1, 0, 'C')
    pdf.cell(30, 8, 'Verde', 1, 2, 'C')
    pdf.cell(-140)
    
    # TABLA DE DISTRIBUCIÓN DE PROMEDIOS POR INDICADOR
    pdf.set_font('Arial', '', 10)
    promedios = promedios_por_indicador(diagnostico)
    for _, row in promedios.iterrows():
        pdf.cell(80, 8, row["indicador"], 1, 0, 'L')
        pdf.cell(30, 8, f'{row["rojo"]}%', 1, 0, 'C')
        pdf.cell(30, 8, f'{row["amarillo"]}%', 1, 0, 'C')
        pdf.cell(30, 8, f'{row["verde"]}%', 1, 2, 'C')
        pdf.cell(-140)

    pdf.add_page()
    pdf.cell(60, 8, 'Análisis de Indicadores', 1, 0, 'C')

    pdf.output(directorio_resultados + f'/informe_{id_facilitador}.pdf', 'F')

