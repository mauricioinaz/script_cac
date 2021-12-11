from fpdf import FPDF
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
from pylab import savefig
from configuracion import ESTRUCTURA_SEMAFORO, DIRECTORIO_ACTUAL, COLORES
import logging


CANTIDAD_RENGLONES = 1
# límites maximos de rango
RANGOS = [.75, .66, .33, .25, 0]

# Función en qué rango está la mayoría de los promedios
def ubicar_rango(promedios):
    mayor = 1
    indicadores_por_rango = []
    total = len(promedios)
    # Asignar rangos 
    #  A   	  B 	  C       D	     E
    #  0      1       2       3      4 
    # >=75	66>75	33>66	25>33	<=25
    for menor in RANGOS:
        indicadores_por_rango.append(len([p for p in promedios if menor < p <= mayor]))
        mayor = menor

    # Si no hay info es un Else?
    if sum(indicadores_por_rango) == 0:
        return 2
    # 0 Indicadores más fuertes:	
    #   A+B>33% y A>16.5% y D+E<33% y E<16.5% y C<33%
    if indicadores_por_rango[0] + indicadores_por_rango[1] > total*0.33 and \
            indicadores_por_rango[0] > total*0.165 and \
            indicadores_por_rango[3] + indicadores_por_rango[4] < total*0.33 and \
            indicadores_por_rango[4] < total*0.165 and \
            indicadores_por_rango[2] < total*0.33:
        return 0
    # 1 Indicadores buenos:	
    #   A+B>33% y D+E<33% y C<33%
    if indicadores_por_rango[0] + indicadores_por_rango[1] > total*0.33 and \
            indicadores_por_rango[3] + indicadores_por_rango[4] < total*0.33 and \
            indicadores_por_rango[2] < total*0.33:
        return 1
    # 3 Indicadores bajos:
    #   D+E>33% y A+B<33% y C<33%
    if indicadores_por_rango[3] + indicadores_por_rango[4] > total*0.33 and \
            indicadores_por_rango[0] + indicadores_por_rango[1] < total*0.33 and \
            indicadores_por_rango[2] < total*0.33:
        return 3
    # 4 Indicadores graves:
    #   D+E>33% y E>16.5% y A+B<33% y C<33%
    if indicadores_por_rango[3] + indicadores_por_rango[4] > total*0.33 and \
            indicadores_por_rango[4] > total*0.165 and \
            indicadores_por_rango[0] + indicadores_por_rango[1] < total*0.33 and \
            indicadores_por_rango[2] < total*0.33:
        return 4
    # 2 Indicadores de atención:	
    #   Else
    return 2

def generar_pay(promedios, directorio_resultados):
    # Cerrar figuras anteriores para mejor manejo de memoria
    plt.close('all')
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = '(-33%)', '(66%-33%)', '(+66%)'

    sizes = [promedios['rojo'].mean(), promedios['amarillo'].mean(), promedios['verde'].mean()]

    explode = [0.1, 0.1, 0.1]

    #            red          yellow       green
    colors = ['#fb0707', '#effb07', '#07fb26']

    _, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ubicacion_imagen = directorio_resultados + '/grafica.png'
    savefig(ubicacion_imagen)
    return ubicacion_imagen

# Rojo: 
#   si los indicadores en verde son menores que 25%, 
#   los indicadores amarillos menos de 33% 
#   los rojos mayores que 40%
# Verde: 
#   si los indicadores en rojo son menores que 25%
#   los indicadores amarillos menos de 40% 
#   los indicadores verdes mayores que 40% 
# Amarillo: 
#   else
def semaforo_por_indicador(rojo, amarillo, verde):
    if verde < 25 and amarillo < 33 and rojo > 40:
        return 'rojo'
    elif rojo < 25 and amarillo < 40 and verde > 40:
        return 'verde'
    else:
        return 'amarillo'

def promedios_por_indicador(diagnostico):
    promedios_indicador = pd.DataFrame()
    for indicador, info_seccion in ESTRUCTURA_SEMAFORO.items():
        preguntas_por_indicador = info_seccion[CANTIDAD_RENGLONES]
        promedios = []
        for _, row in diagnostico.iterrows():
            suma_preguntas = sum([row[indicador + str(n)] for n in range(preguntas_por_indicador)])
            promedio = suma_preguntas / preguntas_por_indicador
            promedios.append(promedio)
        rojo = (len([True for pr in promedios if pr <= 0.33]) / len(promedios) ) * 100
        amarillo = (len([True for pr in promedios if pr > 0.33 and pr <= 0.66]) / len(promedios) ) * 100
        verde = (len([True for pr in promedios if pr > 0.66]) / len(promedios) ) * 100
        semaforo = semaforo_por_indicador(rojo, amarillo, verde)
        promedios_indicador = promedios_indicador.append({
            'indicador' : indicador,
            'rojo' : rojo,
            'amarillo' : amarillo,
            'verde' : verde,
            'semaforo' : semaforo,
            'rango': ubicar_rango(promedios),
            # 'promedios': promedios
        }, ignore_index=True)
        # print(promedios)
        promedios_redondeados = promedios_indicador.round(decimals=2)
    return promedios_redondeados

# Rojo: 
#   si del total de indicadores en verde son menores que 25%, 
#   los indicadores amarillos menos de 33% 
#   los rojos mayores que 40% 
# Verde: 
#   si los indicadores en rojo son menores que 25%, 
#   los indicadores amarillos menos de 40% 
#   los indicadores verdes mayores que 40% 
# Amarillo: else
def gradiente_social(semaforos):
    if (semaforos.count('verde') < len(semaforos)*0.25 and 
            semaforos.count('amarillo') < len(semaforos)*0.33 and 
            semaforos.count('rojo') > len(semaforos)*0.4):
        return 'rojo'
    elif (semaforos.count('rojo') < len(semaforos)*0.25 and
            semaforos.count('amarillo') < len(semaforos)*0.4 and
            semaforos.count('verde') > len(semaforos)*0.4):
        return 'verde'
    else:
        return 'amarillo'

class PDF(FPDF):
    def header(self):
        # Importar hoja con Membrete
        self.image(DIRECTORIO_ACTUAL + '/IMAGENES/Fondo.jpeg', 0, 0, 210, 297)

def generar_reporte(diagnostico, directorio_resultados):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)

    pdf.cell(50)
    id_facilitador = diagnostico['ID_Facilitador'].iloc[0]
    # TÍTULO
    pdf.cell(90, 3, " ", 0, 2, 'C')
    pdf.cell(75, 10, f"Informe de Facilitador", 0, 2, 'C')
    pdf.cell(75, 10, f"#{id_facilitador}", 0, 2, 'C')
    pdf.cell(-30)
    pdf.cell(90, 15, " ", 0, 2, 'C')

    #
    # INFO DEL FACILITADOR
    #
    pdf.set_font('Arial', 'B', 14)
    # Territorio
    pdf.cell(50, 10, 'Territorio:', 1, 0, 'R')
    territorio = diagnostico['Territorio'].iloc[0]
    pdf.cell(70, 10, territorio, 1, 2, 'C')
    pdf.cell(-50)
    # # Año de aplicación:
    pdf.cell(50, 10, 'Año de aplicación:', 1, 0, 'R')
    fecha_excel = diagnostico['Fecha_Aplicacion'].iloc[0]
    # convertir formato fecha excel a texto
    if type(fecha_excel) is int:
        fecha = xlrd.xldate_as_datetime(fecha_excel, 0)
        anio = str(fecha.year)
    else:
        anio = 'fecha no disponible'
        f'{fecha_excel} '
        logging.warning(f'Fecha " {fecha_excel}" no válida - en pestaña "{diagnostico["Nombre_Pestania"].iloc[0]}" "{diagnostico["Nombre_Archivo"].iloc[0]}" ')
        
    pdf.cell(70, 10, anio, 1, 2, 'C')
    pdf.cell(-50)
    # Iteración:
    pdf.cell(50, 10, 'Iteración:', 1, 0, 'R')
    iteracion = diagnostico['Iteracion'].iloc[0]
    pdf.cell(70, 10, iteracion, 1, 2, 'C')
    pdf.cell(-50)

    promedios = promedios_por_indicador(diagnostico)
    color_gradiente = gradiente_social(promedios['semaforo'].to_list())

    pdf.cell(50, 10, 'Gradiente Social:', 1, 0, 'R')
    pdf.set_fill_color(*COLORES[color_gradiente])
    pdf.cell(70, 10, ' ', 1, 2, 'C', fill=True)
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-60)


    # ENCABEZADOS INDICADORES
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 8, 'Indicador', 1, 0, 'L')
    pdf.cell(25, 8, 'Rojo', 1, 0, 'C')
    pdf.cell(25, 8, 'Amarillo', 1, 0, 'C')
    pdf.cell(25, 8, 'Verde', 1, 0, 'C')
    pdf.cell(25, 8, 'Semáforo', 1, 2, 'C')
    pdf.cell(-155)

    # TABLA DE DISTRIBUCIÓN DE PROMEDIOS POR INDICADOR
    pdf.set_font('Arial', '', 10)
    for _, row in promedios.iterrows():
        pdf.cell(80, 8, row["indicador"], 1, 0, 'L')
        pdf.cell(25, 8, f'{row["rojo"]}%', 1, 0, 'C')
        pdf.cell(25, 8, f'{row["amarillo"]}%', 1, 0, 'C')
        pdf.cell(25, 8, f'{row["verde"]}%', 1, 0, 'C')
        pdf.set_fill_color(*COLORES[row["semaforo"]])
        pdf.cell(25, 8, ' ', 1, 2, 'C', fill=True)
        pdf.cell(-155)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)

    pdf.cell(50)
    # TÍTULO
    pdf.cell(90, 3, " ", 0, 2, 'C')
    pdf.cell(75, 10, f"Gráfica de Promedios", 0, 2, 'C')
    pdf.cell(75, 10, f"Totales", 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-80)
    ubicacion_imagen = generar_pay(promedios, directorio_resultados)
    pdf.image(ubicacion_imagen, x = None, y = None, w = 0, h = 0, type = '', link = '')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    # Título PÁGINA 2
    pdf.cell(57)
    pdf.cell(90, 7, " ", 0, 2, 'C')
    pdf.cell(60, 8, 'Análisis de Indicadores', 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(90, 10, " ", 0, 2, 'C')
    pdf.cell(-57)

    TITULOS_RANGOS = [
        'Más fuertes',    # 0
        'Buenos',         # 1
        'de Atención',    # 2
        'Bajos',          # 3
        'Graves',         # 4
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
