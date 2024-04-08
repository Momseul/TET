# TET
Sistema distribuido de archivos basado en GFS, el sistema soporta la subida y almacenamientos de archivos devididos en bloques para su posterior lectura.
El sistema tiene 3 componentes principales: datanode, namenode y cliente; el cliente es quien se encarga de las operación de particionamiento, subida, busqueda, descarga y reensable de archivos. El namenode es quien gestiona las replicas y gestionar la distribución de archivos, además de controlar la metadata correspondiente; por ultimo el datanode es quien se encarga de almacenar y distribuir los bloques a sus pares.

hghfg


### Modo de uso
Todos los modulos necesarios para el correcto desliegue del sistema se encuntran el el archivo requirements.txt

### Uso del namenode
``` python -m namenode.namenode ```

### Uso del datanode 
```python -m datanode.main --datanode_address "<datanode ip_address>"```

### Uso del cliente
```python -m client.main "<ip_address>" "<port>" "<-g || -p>" "<file>"```


opción -p: sube el archivo al datanode proporcionado por el usuario



opción -g: obtiene los bloques almacenados en el datanode ubicado cuya dirección ip es proporcionada por el usuario y los reensambla despues de obtenerlos todos. 
