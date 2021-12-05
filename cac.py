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
                          ESTRUCTURA_SEMAFORO, ITERACIONES, DIRECTORIO_ACTUAL\


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
    resultados_actuales = directorio_resultados + '/' + f'RESULTADOS_{time.strftime("%Y-%m-%d-%H:%M.%S")}'
    makedirs(resultados_actuales)
    return  resultados_actuales

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
                    for sum in range(info_seccion[CANTIDAD_RENGLONES]):
                        renglon = inicio_renglon + sum
                        nombre_renglon = col+str(sum)
                        renglon_nuevo[nombre_renglon] = datos_leidos.at[renglon, COL_SEMAFORO]

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
    logging.basicConfig(filename=f'LOGS/errores_{time.strftime("%Y-%m-%d-%H:%M.%S")}.log', 
                        filemode='w', 
                        format='%(levelname)s - %(message)s', 
                        level=logging.INFO)

    directorio_resultados = obtener_directorio_resultados()
    resultados = analizar_xlsx(iteracion, directorio_resultados)
    
    # Obtener listado de facilitadores y generar reporte para cada uno
    facilitadores = resultados['ID_Facilitador'].unique()
    print('')
    print (f'Generando Reportes para {len(facilitadores)} facilitadores')
    log_title('ERRORES DE GENERACIÓN DE REPORTES')
    contador_de_errores = 0
    for facilitador in tqdm(facilitadores):
        try:
            if not isnan(facilitador):
                diagnosticos_facilitador = resultados.loc[resultados['ID_Facilitador'] == facilitador]
                generar_reporte(diagnosticos_facilitador, directorio_resultados)
            else:
                logging.error(f'INFORME NO GENERADO - No se pudo obtener el ID de un facilitador por estar vacío - {facilitador}')
                contador_de_errores += 1
        except TypeError:
            logging.error(f'INFORME NO GENERADO - Numero invalido del facilitador - {facilitador} - isNAN')
            contador_de_errores += 1
    
    # Registrar INFO FINAL
    print('')
    reportes_generados = f'Se generaron exitosamente {len(facilitadores)-contador_de_errores} reportes de {len(facilitadores)} facilitadores'
    reportes_errores = f'No se generaron {contador_de_errores} reportes por errores de ID'
    print(reportes_generados)
    print(reportes_errores)
    log_title('INFO GENERAL')
    logging.info(reportes_generados)
    logging.info(reportes_errores)

if __name__ == "__main__":
    main()
