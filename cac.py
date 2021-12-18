import time
import logging
from tqdm import tqdm
from os import listdir, makedirs
from os.path import isfile, join, exists
from datetime import datetime
import pandas as pd
from numpy import isnan
from reportes import generar_reporte
from configuracion import COL_INFO, COL_SEMAFORO, ESTRUCTURA_INFO, \
                          ESTRUCTURA_SEMAFORO, ITERACIONES, DIRECTORIO_ACTUAL,\
                          NOMBRE_XLSX_LISTADO_FACILITADORES, SHEET_LISTADO_FACILITADORES, \
                          COLS_LISTADO_FACILITADORES


INICIO_RENGLON = 0
CANTIDAD_RENGLONES = 1

# regresa un arreglo con todos los nombres de los archivos dentro de la carpeta /ARCHIVOS
# Y regresa la ubicacion de la carpeta
def obtener_lista_xlsx(carpeta):
    directorio_archivos = DIRECTORIO_ACTUAL + '/ARCHIVOS' + carpeta
    archivos = [f for f in listdir(directorio_archivos) if isfile(join(directorio_archivos, f))]
    # filtra solo .xlsx e ignora los abiertos
    archivos_xlsx = [a for a in archivos if (a.endswith('.xlsb') or a.endswith('.xls') or a.endswith('.xlsx')) and not a.startswith('~')]
    return archivos_xlsx, directorio_archivos+'/'


# Checa si existe el directorio Resultados y si no lo crea
# y Crea una carpeta nueva con la fecha para los resultados del momento
def obtener_directorio_resultados():
    directorio_resultados = DIRECTORIO_ACTUAL + '/RESULTADOS'
    if not exists(directorio_resultados):
        makedirs(directorio_resultados)
    resultados_actuales = directorio_resultados + '/' + f'RESULTADOS_{time.strftime("%Y-%m-%d-%H%M%S")}'
    makedirs(resultados_actuales)
    return  resultados_actuales

# Obtener el listado de facilitadores a partir de excel
def obtener_listado_facilitadores():
    path = DIRECTORIO_ACTUAL + '/ARCHIVOS' + '/' + NOMBRE_XLSX_LISTADO_FACILITADORES
    xls = pd.ExcelFile(path)
    listado_facilitadores = xls.parse(usecols=COLS_LISTADO_FACILITADORES, sheet_name=SHEET_LISTADO_FACILITADORES)
    return listado_facilitadores


# Recorre cada archivo y extae las celdas de INFO y SEMAFORO
# regresa un xlsx con los resultados
def analizar_xlsx(iteracion, directorio_resultados):
    log_title('ERRORES DE LECTURA DE ARCHIVOS')
    resultados = pd.DataFrame()

    # Recorrer cada carpeta Inicia / Intermedia / Final
    for carpeta in ITERACIONES[:iteracion]:
        # TODO Mensaje si no existen las carpetas
        archivos, directorio_archivos = obtener_lista_xlsx('/'+carpeta)

        print(f'Analizando {len(archivos)} archivos en la carpeta: {carpeta}')
        for archivo in tqdm(archivos):
            path = directorio_archivos + archivo

            xls = pd.ExcelFile(path)
            # Recorrer todas las Pestañas de cada excel
            for sheet_name in xls.sheet_names:
                # Ignorar pestaña GRAFICAS
                if sheet_name == "GRAFICAS":
                    continue

                # Leer datos de la pestaña
                datos_leidos = xls.parse(header=None, usecols=[COL_INFO,COL_SEMAFORO], sheet_name=sheet_name)
                
                # No registrar renglón de datos si Nombre_CAC no existe
                try:
                    Nombre_CAC_vacio = pd.isnull(datos_leidos[COL_INFO].iloc[ESTRUCTURA_INFO['Nombre_CAC']])
                    if Nombre_CAC_vacio:
                        logging.warning(f'Pestaña "{sheet_name}" parece estar vaciá en archivo "{archivo}"')
                        continue
                # Caso cuando hoja de excel está mal?
                except KeyError:
                    logging.error(f'KEYERROR - Pestaña "{sheet_name}" parece estar vaciá en archivo "{archivo}"')
                    continue

                # Extraer Info general
                renglon_nuevo = {}
                for col, renglon in ESTRUCTURA_INFO.items():
                    renglon_nuevo[col] = datos_leidos.at[renglon, COL_INFO]
                renglon_nuevo['Nombre_Archivo'] = archivo
                renglon_nuevo['Nombre_Pestania'] = sheet_name

                # Extraer para INICIAL, INTERMEDIA y FINAL agregando desfase de columnas
                # for iter, desfase in enumerate(DESFASES[:iteracion]):
                #     renglon_nuevo = info_general
                renglon_nuevo['Iteracion'] = carpeta

                # Extraer datos de semáforo de sección
                for col, info_seccion in ESTRUCTURA_SEMAFORO.items():
                    inicio_renglon = info_seccion[INICIO_RENGLON]
                    suma = 0
                    for sum in range(info_seccion[CANTIDAD_RENGLONES]):
                        renglon = inicio_renglon + sum
                        nombre_renglon = col+str(sum)
                        renglon_nuevo[nombre_renglon] = datos_leidos.at[renglon, COL_SEMAFORO]
                        suma += datos_leidos.at[renglon, COL_SEMAFORO]
                    renglon_nuevo[col+'_Promedio'] = suma/info_seccion[CANTIDAD_RENGLONES]

                # Agregar renglón de datos a tabla resultados
                resultados = resultados.append(renglon_nuevo, ignore_index=True)

    # Guardar Archivo en Carpeta Resultados, usando resultados_fecha_hora como nombre
    nombre_resultados = f'resultados_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.xlsx'
    resultados.to_excel(directorio_resultados + '/' + nombre_resultados, sheet_name='resultados')

    print('')
    print(f'Se generó el archivo: {nombre_resultados}')

    return resultados

# Para formato del LOG
def log_title(title):
    logging.info(f'')
    logging.info(f'')
    logging.info(f'--- {title} --- ')
    logging.info(f'')
    logging.info(f'')

def main():
    # Solicitar iteraciones a Usuario
    iteracion = 0
    print('Qué periodos quieres analizar?')
    while iteracion not in [1,2,3]:
        print('1 (Inicial) / 2 (Inicial e Intermedio) / 3 (Inicial, Intermedio y Final)')
        iteracion = int(input('Elige un Número: '))
        print(iteracion)

    # Configurar archivo de errores
    logging.basicConfig(filename=f'LOGS/errores_{time.strftime("%Y-%m-%d-%H%M%S")}.log', 
                        filemode='w', 
                        format='%(levelname)s - %(message)s', 
                        level=logging.INFO)

    directorio_resultados = obtener_directorio_resultados()
    listado_facilitadores = obtener_listado_facilitadores()
    resultados = analizar_xlsx(iteracion, directorio_resultados)
    
    # Obtener listado de facilitadores y generar reporte para cada uno
    facilitadores = resultados['ID_Facilitador'].unique()
    print('')
    print (f'Generando Reportes para {len(facilitadores)} facilitadores')
    log_title('ERRORES DE GENERACIÓN DE REPORTES')
    contador_de_errores = 0
    contador_de_facilitadores_sin_datos = 0
    #resultados = pd.DataFrame()
    listado_filtrado = pd.DataFrame()
    print(resultados)
    for facilitador in tqdm(facilitadores):
        try:
            if not isnan(facilitador):
                datos_facilitador = listado_facilitadores.loc[listado_facilitadores['ID'] == facilitador]
                listado_filtrado = listado_filtrado.append(datos_facilitador, ignore_index=True)
                diagnosticos_facilitador = resultados.loc[resultados['ID_Facilitador'] == facilitador]
                generar_reporte(diagnosticos_facilitador, datos_facilitador, directorio_resultados)
                if datos_facilitador.empty:
                    contador_de_facilitadores_sin_datos += 1
            else:
                archivos = resultados.loc[resultados['ID_Facilitador'] == facilitador]["Nombre_Archivo"].unique()
                pestanias = resultados.loc[resultados['ID_Facilitador'] == facilitador]["Nombre_Pestania"].unique()
                logging.error(f'INFORME NO GENERADO ELSE - No se pudo obtener el ID de un facilitador - {facilitador} - en archivos {archivos} en pestaña {pestanias}')
                contador_de_errores += 1
        # except KeyError:
        #     logging.error('truena por KeyError')
        except TypeError:
            archivos = resultados.loc[resultados['ID_Facilitador'].isnull()]["Nombre_Archivo"].unique()
            pestanias = resultados.loc[resultados['ID_Facilitador'].isnull()]["Nombre_Pestania"].unique()
            logging.error(f'INFORME NO GENERADO TypeError - Numero invalido del facilitador - {facilitador} - en archivos {archivos} en pestanias {pestanias}')
            contador_de_errores += 1
    
    # Excel con la lista de facilitadores que SÍ se les generó un reporte
    listado_filtrado.to_excel(DIRECTORIO_ACTUAL+'/RESULTADOS' +'/listadoDeFacilitadoresConReporte.xlsx', sheet_name='listado_filtrado')

    # Registrar INFO FINAL
    print('')
    reportes_generados = f'Se generaron exitosamente {len(facilitadores)-contador_de_errores} reportes de {len(facilitadores)} facilitadores'
    reportes_errores = f'No se generaron {contador_de_errores} reportes por errores de ID'
    reportes_errores_datos = f'No se encontró el nombre de {contador_de_facilitadores_sin_datos} facilitadores en el listado'
    print(reportes_generados)
    print(reportes_errores)
    log_title('INFO GENERAL')
    logging.info(reportes_generados)
    logging.info(reportes_errores)
    logging.info(reportes_errores_datos)

if __name__ == "__main__":
    main()
