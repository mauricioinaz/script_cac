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
    'Identidad_Valores_Compartidos': [17, 3],
    'Consecucion_Eficiente_Objetivos': [26, 2],
    'Integracion_Resolucion_Conflictos': [34, 6],
    'Participacion_Relaciones_Democraticas': [46, 3],
    'Liderazgo_Positivo': [56, 3],
    'Capacidad_Gestion_Art_Autonomia': [66, 3],
    'Construccion_Tejido_Social': [75, 2],
    'Soberania_Alimentaria': [88, 4],
    'Trabajo_Equipo_Emprendimiento_Coop': [100, 4],
    'Cultura_Ahorro_Finanzas_Sociales': [112, 4],
    'Equidad_Genero': [122, 4],
    'Apr_Labores_Culturales': [136, 3],
    'Habitos_Consumo_Descarte': [144, 3],
    'Acciones_Saberes_Cuidado_Restauracion': [152, 3],
    'Salud_Comunitaria': [161, 3]
}

# Nombres de carpetas de las iteraciones
ITERACIONES = ['INICIAL', 'INTERMEDIO', 'FINAL']

# Nombres de las pestañas que se extraerán
# CAC1, CAC2, CAC3...
SHEETS_NAME = 'CAC'

# UBICACIÓN DIRECTORIO
DIRECTORIO_ACTUAL = abspath(getcwd())

NOMBRE_XLSX_LISTADO_FACILITADORES = 'ListadoFacilitadores.xlsx'
SHEET_LISTADO_FACILITADORES = 'Hoja1'
COLS_LISTADO_FACILITADORES = [1,2,3,4]