# Script para extraer datos CAC

Para instalar script crear un ambiente virtual de Python e instalar dependencias:

```
python -m venv env 
pip install -r requirements.txt
```



### Ejecución

Agregar los archivos a analizar en la carpeta de `/ ARCHIVOS`

Ejecutar el script:

```
python cac.py
```



### CONFIGURAR

Si la estructura de las encuestas cambia, se debe actualizar las variables de  `constantes.py` . 

```python
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
    ...
}

# Los nombres de las pestañas
SHEETS = ['Diagnostico Inicial', 'Diagnostico Intermedio', 'Diagnostico Final']
```

### POR HACER:
Falta:
+ [ ] Generar archivo de errores
+ [ ] Cachar errores cuando una sección está vacía
+ [ ] Generar error cuando la info leída no es del tipo esperado
+ [ ] Mejorar apariencia de arhivo resultados