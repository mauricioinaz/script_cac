# Script para extraer datos CAC

Para instalar script crear un ambiente virtual de Python e instalar dependencias:

```
python -m venv env
pip install -r requirements.txt
pip install tqdm
```



### Ejecución

Agregar los archivos a analizar en la carpeta de `/ ARCHIVOS`

Ejecutar el script:

```
source env/bin/activate
python cac.py
```



### CONFIGURAR

Si la estructura de las encuestas cambia, se debe actualizar las variables de  `configuracion.py` .

```python
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
    ...
}

# DESFASE PARA EXTRAER SECCIÓN
#            [Inicial, Interm, Final]
DESFASES = [0, 177, 354]

# Nombres de las pestañas que se extraerán
# CAC1, CAC2, CAC3...
SHEETS_NAME = 'CAC'

```

### POR HACER:
Falta:
+ [ ] Generar archivo de errores
+ [ ] Cachar errores cuando una sección está vacía
+ [ ] Generar error cuando la info leída no es del tipo esperado
+ [ ] Mejorar apariencia de arhivo resultados
