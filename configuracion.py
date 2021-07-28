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
    'Nombre_Tecnico': 2,
    'ID_CAC': 3,
    'Ruta': 4,
    'Territorio': 5
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

# DESFASE PARA EXTRAER SECCIÓN
#            [Inicial, Interm, Final]
DESFASES = [0, 177, 354]

# Nombres de las pestañas que se extraerán
# CAC1, CAC2, CAC3...
SHEETS_NAME = 'CAC'
