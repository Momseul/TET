# TET - Sistema de Archivos Distribuidos (DFS) Minimalista
El sistema TET es una implementación minimalista de un Sistema de Archivos Distribuidos (DFS) basado en Google File System (GFS) y Hadoop File System (HDFS), el sistema soporta la subida y almacenamientos de archivos divididos en bloques para su posterior lectura.
El sistema tiene 3 componentes principales: datanode, namenode y cliente; el cliente es quien se encarga de las operación de particionamiento, subida, busqueda, descarga y reensable de archivos. El namenode es quien gestiona las replicas y gestionar la distribución de archivos, además de controlar la metadata correspondiente; por ultimo el datanode es quien se encarga de almacenar y distribuir los bloques a sus pares.

## Componentes

**Name Node Leader:**
- Funciona como el cerebro del sistema, gestionando el espacio de nombres, la metadata de los archivos y coordina la distribución de bloques y las replicas entre los DataNodes.
- Coordina las operaciones de archivo, como la apertura, la lectura y la escritura, y supervisa la distribución y replicación de bloques.

**Data Nodes:**
- Almacena los datos reales en forma de bloques
- Trabaja bajo las instrucciones y coordinación del NameNode para gestionar la replicación y permitir operaciones eficientes de lectura/escritura.

**Cliente:**
- Interfaz de usuario para interactuar con el sistema DFS, permitiendo a los usuarios almacenar, recuperar y buscar archivos.
- Divide los archivos en bloques para su almacenamiento y reensambla los bloques durante la recuperación.


## Características Principales
Distribución basada en Bloques: Los archivos se dividen en bloques (chunks) que se distribuyen y replican entre varios nodos (DataNodes), mejorando la disponibilidad y tolerancia a fallos.
- Gestión Centralizada de Metadata: Un NameNode centraliza la gestión de metadatos, manteniendo un registro de la ubicación de todos los bloques y su replicación.
- Interacción Cliente-Datanode: La escritura y lectura de archivos se realiza directamente entre el Cliente y los DataNodes, optimizando la transferencia de datos.
- Replicación y Tolerancia a Fallos: Cada bloque se replica en múltiples DataNodes, asegurando la disponibilidad de datos frente a fallos de nodos.


### Modo de uso
#### Requisitos
- Python 3.8 o superior
- gRPC
- Instalar dependencias desde `requirements.txt`

### Uso del namenode
``` python -m namenode.namenode ```

### Uso del datanode 
```python -m datanode.main --datanode_address "<datanode ip_address>"```

### Uso del cliente
```python -m client.main "<ip_address>" "<port>" "<-g || -p>" "<file>"```

Subir un archivo:
- opción `-p`: sube el archivo al datanode proporcionado por el usuario

Descargar y reensamblar un archivo:
- opción `-g`: obtiene los bloques almacenados en el datanode ubicado cuya dirección ip es proporcionada por el usuario y los reensambla despues de obtenerlos todos. 

---

Para un mayor entendimiento de la arquitectura implementada y de los fundamentos de sistemas de archivos distribuidos basados en bloques, incluyendo su inspiración en GFS y HDFS, consulte la [Wiki](https://github.com/Momseul/TET/wiki) del proyecto.
