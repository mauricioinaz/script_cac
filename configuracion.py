from os import getcwd
from os.path import abspath
#
# INFO PARA CONFIGURAR RENGLONES Y COLUMNAS A LEER
#

# Indicar las columnas en las que se encuentran los datos
COL_INFO = 1
COL_SEMAFORO = 7

# Indicar el número de renglón a leer de la COL_INFO
ESTRUCTURA_INFO = {
    'Nombre_CAC': 0,
    'Fecha_Aplicacion': 1,
    'ID_Tecnico': 2,
    'ID_CAC': 3,
    'ID_Facilitador': 4,
    'Territorio': 5
#    'Correo_Tecnico_Social': 6
}

COLORES = {
    'rojo': [238, 9, 26],
    'amarillo': [255, 255, 0], 
    'verde': [0, 255, 0]
}

# En un arreglo indicar renglón de inicio de cada seccion, y la cantidad de renglones
# a anlizar de la COL_SEMAFORO
ESTRUCTURA_SEMAFORO = {
#   'Nombre_de_la_Seccion': [InicioRenglon, #DeRenglones]
    'Identidad y valores compartidos': [17, 3],
    'Consecución eficiente de los objetivos': [26, 2],
    'Integración y resolución de conflictos': [34, 6],
    'Participación y relaciones democráticas': [46, 3],
    'Liderazgo positivo': [56, 3],
    'Capacidad de gestión, articulación y autonomía': [66, 3],
    'Construcción del tejido social': [75, 2],
    'Soberanía alimentaria': [88, 4],
    'Trabajo en equipo y emprendimiento cooperativo': [100, 4],
    'Cultura del ahorro y finanzas sociales': [112, 4],
    'Equidad de género': [122, 4],
    'Apropiación de labores culturales de cultivo': [136, 3],
    'Hábitos de consumo y descarte': [144, 3],
    'Acciones de cuidado al medio ambiente': [152, 3],
    'Salud comunitaria': [161, 3]
}

# Nombres de carpetas de las iteraciones
ITERACIONES = ['INICIAL_PRUEBA', 'INTERMEDIO', 'FINAL']

# Nombres de las pestañas que se extraerán
# CAC1, CAC2, CAC3...
SHEETS_NAME = 'CAC'

# UBICACIÓN DIRECTORIO
DIRECTORIO_ACTUAL = abspath(getcwd())

NOMBRE_XLSX_LISTADO_FACILITADORES = 'ListadoFacilitadores.xlsx'
SHEET_LISTADO_FACILITADORES = 'Hoja1'
COLS_LISTADO_FACILITADORES = [1,2,3,4]