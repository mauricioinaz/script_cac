#
# INFO PARA CONFIGURAR RENGLONES Y COLUMNAS A LEER
#

# Indicar las columnas en las que se encuentran los datos
COL_INFO = 1
COL_SEMAFORO = 7

# Indicar el número de renglón a leer de la COL_INFO
ESTRUCTURA_INFO = {
    'NombreCac': 0,
    'Fecha_Aplicacion': 1,
    'Nombre_Tecnico': 2
}

# En un arreglo indicar renglón de inicio de cada seccion, y la cantidad de renglones 
# a anlizar de la COL_SEMAFORO
ESTRUCTURA_SEMAFORO = {
    # 'Nombre': [InicioRenglon, CantidadDeRenglones]
    'IdentValores': [13, 3],
    'ConsecucionObjetivos': [22, 2],
    'IntegracionResolucion': [30, 6],
    'ParticipacionRelaciones': [42, 3],
    'LiderazgoPositivo': [52, 3],
    'CapacidadArtAutonomia': [62, 3],
    'ConstruccionTejido': [71, 2],
    'SoberaniaAlimentaria': [84, 4],
    'TrabajoEquipo': [96, 4],
    'CulturaAhorroFinanzasSociales': [108, 4],
    'EquidadGenero': [118, 4],
    'AprLaboresCulturales': [132, 3],
    'HabitosConsumo': [140, 3],
    'AccionesCuidado': [148, 3],
    'SaludComunitaria': [157, 3]
}

# Los nombres de las pestañas
SHEETS = ['Diagnostico Inicial', 'Diagnostico Intermedio', 'Diagnostico Final']
