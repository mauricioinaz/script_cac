from os import listdir, getcwd, makedirs
from os.path import isfile, join, abspath, exists
from datetime import datetime
import pandas as pd
from constantes import COL_INFO, COL_SEMAFORO, ESTRUCTURA_INFO, ESTRUCTURA_SEMAFORO, SHEETS

INICIO_RENGLON = 0
CANTIDAD_RENGLONES = 1

# regresa un arreglo con todos los nombres de los archivos dentro de la carpeta /ARCHIVOS 
# Y regresa la ubicacion de la carpeta
def obtener_lista_xlsx():
    directorio_actual = abspath(getcwd())
    directorio_archivos = directorio_actual + '/ARCHIVOS'
    archivos = [f for f in listdir(directorio_archivos) if isfile(join(directorio_archivos, f))]
    # filtra solo .xlsx e ignora los abiertos
    archivos_xlsx = [a for a in archivos if a.endswith('.xlsx') and not a.startswith('~')]
    return archivos_xlsx, directorio_archivos+'/'


# Checa si existe el directorio Resultados y si no lo crea
def obtener_directorio_resultados():
    directorio_actual = abspath(getcwd())
    directorio_resultados = directorio_actual + '/RESULTADOS'
    if not exists(directorio_resultados):
        makedirs(directorio_resultados)
    return directorio_resultados

# Recorre cada archivo y extae las celdas de INFO y SEMAFORO 
# regresa un xlsx con los resultados
def analizar_xlsx(archivos, directorio_archivos, iteraciones):
    resultados = pd.DataFrame()
    for archivo in archivos:
        path = directorio_archivos + archivo
        # Recorrer cada Sheet del Excel
        for sh in SHEETS[:iteraciones]:
            datos_leidos = pd.read_excel(path, header=None, usecols=[COL_INFO,COL_SEMAFORO], sheet_name=sh)
            # TODO: Revisar que se extrajeron las columnas o regresar error!
            renglon_nuevo = {}
            # Extraer info
            for col, renglon in ESTRUCTURA_INFO.items():
                renglon_nuevo[col] = datos_leidos.at[renglon, COL_INFO]
            renglon_nuevo['Nombre_Archivo'] = archivo
            renglon_nuevo['Iteracion'] = sh
            # Extraer datos
            for col, info_seccion in ESTRUCTURA_SEMAFORO.items():
                inicio_renglon = info_seccion[INICIO_RENGLON]
                for sum in range(info_seccion[CANTIDAD_RENGLONES]):
                    renglon = inicio_renglon + sum
                    nombre_renglon = col+str(sum)
                    renglon_nuevo[nombre_renglon] = datos_leidos.at[renglon, COL_SEMAFORO]
            # Agregar nuevo Renglón
            resultados = resultados.append(renglon_nuevo, ignore_index=True)
    # print(resultados)

    # Guardar Archivo en Carpeta Resultados, usando resultados_fecha_hora como nombre
    directorio_resultados = obtener_directorio_resultados()
    nombre_resultados = f'resultados_{datetime.now().strftime("%d-%m-%Y_%H%M%S")}.xlsx'
    resultados.to_excel(directorio_resultados + '/' + nombre_resultados, sheet_name='resultados')
    print('')
    print(f'Se generó el archivo: {nombre_resultados}')


def main():
    archivos, directorio_archivos = obtener_lista_xlsx()
    if len(archivos) == 0:
        print('No se encontraron xlsx en la carpeta de ARCHIVOS.')
        return None

    iteraciones = 0
    print('Qué periodos quieres analizar?')
    while iteraciones not in [1,2,3]:
        print('1 (Inicial) / 2 (Inicial e Intermedio) / 3 (Inicial, Intermedio y Final)')
        iteraciones = int(input('Elige un Número: '))
        print(iteraciones)

    print(f'Analizando {len(archivos)} archivos')
    analizar_xlsx(archivos, directorio_archivos, iteraciones)

if __name__ == "__main__":
    main()