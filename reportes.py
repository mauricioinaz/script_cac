from fpdf import FPDF
import pandas as pd
from configuracion import ESTRUCTURA_SEMAFORO

CANTIDAD_RENGLONES = 1

# Función en qué rango está la mayoría de los promedios
# posibles resutlados:
# 0:  más fuertes:	Indicadores más veces con 75% o más	
# 1:  buenos:	Indicadores más veces entre 66% y 75%	
# 2:  de atención:	Indicadores más veces entre 33% y 66%	
# 3:  bajos:	Indicadores más veces entre 25% y 33%	
# 4:  graves:	Indicadores más veces entre 0% y 25%
# límites maximos de rango
#         0     1    2    3   4
RANGOS = [.75, .66, .33, .25, 0]
def ubicar_rango(promedios):
    mayor = 1
    indicadores_por_rango = []
    for menor in RANGOS:
        indicadores_por_rango.append(len([p for p in promedios if menor < p < mayor]))
        mayor = menor
    return indicadores_por_rango.index(max(indicadores_por_rango))


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
            'verde' : (len([True for pr in promedios if pr > .66]) / len(promedios) ) * 100,
            'rango': ubicar_rango(promedios)
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
    pdf.set_font('Arial', 'B', 24)
    # Título PÁGINA 2
    pdf.cell(60)
    pdf.cell(60, 8, 'Análisis de Indicadores', 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-60)

    TITULOS_RANGOS = [
        'Más fuertes (mayoría en 75% o más)',
        'Buenos (mayoría entre 66% o 75%)',
        'de Atención (mayoría entre 33% o 66%)',
        'Bajos (mayoría entre 25% o 33%)',
        'Graves (mayoría entre 0% o 25%)',
        ]
    
    for rango, rango_texto in enumerate(TITULOS_RANGOS):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(70, 10, rango_texto, 1, 0, 'L')
        en_rango = promedios.loc[promedios['rango'] == rango]
        indicadores_en_rango = ', '.join(en_rango['indicador'].tolist()) 
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(100, 10, indicadores_en_rango, 1, 2, 'C')
        # pdf.cell(-0)

    pdf.output(directorio_resultados + f'/informe_{id_facilitador}.pdf', 'F')

