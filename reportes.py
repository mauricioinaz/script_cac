from fpdf import FPDF

# Territorio:				
# Año de aplicación:				
# Iteración:				
# ID Facilitador:				
# Gradiente social:	Rojo: si los indicadores en verde son menores que 33% y los rojos mayores que 33% | Verde: si los indicadores en rojo son menores que 25% y los indicadores verdes mayores que 40% | Amarillo: else			

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
    # INFO DEL FACILITADOR
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(50, 10, 'Territorio', 1, 0, 'R')
    pdf.cell(40, 10, 'Pantano', 1, 2, 'C')
    pdf.cell(-50)
    pdf.cell(50, 10, 'Año de aplicación:', 1, 0, 'R')
    pdf.cell(40, 10, '...FECHA...', 1, 2, 'C')
    pdf.cell(-50)
    pdf.cell(50, 10, 'Iteración', 1, 0, 'R')
    iteracion = diagnostico['Iteracion'].iloc[0]
    pdf.cell(40, 10, iteracion, 1, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-60)
    pdf.set_font('Arial', 'B', 12)
    # ENCABEZADOS INDICADORES
    pdf.cell(60, 10, 'Indicador', 1, 0, 'L')
    pdf.cell(30, 10, 'Rojo', 1, 0, 'R')
    pdf.cell(30, 10, 'Amarillo', 1, 0, 'R')
    pdf.cell(30, 10, 'Verde', 1, 2, 'C')

    pdf.set_font('Arial', '', 11)
    pdf.cell(-120)
    # promedios de ese indicador de cada renglón
    # porcentaje promedios que están abajo de 33%
    promedios = []
    for index, row in diagnostico.iterrows():
        promedio = (row['Identidad_Valores_Compartidos0'] + row['Identidad_Valores_Compartidos1'] + row['Identidad_Valores_Compartidos2'])/3
        promedios.append(promedio)
    pdf.cell(60, 10, 'Identidad Valores Compartidos', 1, 0, 'L')
    rojos = (len([True for pr in promedios if pr < 0.33]) / len(promedios) ) * 100
    pdf.cell(30, 10, f'{rojos}%', 1, 0, 'R')
    amarillos = (len([True for pr in promedios if (0.33 < pr < .66)]) / len(promedios) ) * 100
    pdf.cell(30, 10, f'{amarillos}%', 1, 0, 'R')
    verdes = (len([True for pr in promedios if pr > .66]) / len(promedios) ) * 100
    pdf.cell(30, 10, f'{verdes}%', 1, 2, 'C')

    pdf.output(directorio_resultados + f'/informe_{id_facilitador}.pdf', 'F')