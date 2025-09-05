En este primer examen harán un programa con la arquitectura cliente-servidor en dos archivos. El objetivo es evaluar su conocimiento a la hora de implementar esta arquitectura y para esto realizarán las siguientes actividades:

Instalen: `pip install pandas`
1. Crear un servidor como lo hemos visto en clase que se comunique con un cliente. Pueden usar RPCs o Sockets, ambos son válidos.
2. El servidor leerá un archivo llamado DB.csv, este archivo se los voy a proporcionar.
    1. El archivo es separado por comas y lo pueden leer con pandas. Usen `pd.read_csv(path_al_archivo)`.
    2. Las columnas del archivo son:
        1. Nombre
        2. Password
        3. Genero
        4. Edad
        5. Email
        6. Carrera
3. El servidor debe ser capaz de leerlo y de editarlo para añadir nuevos datos.
    1. Estos datos pueden provenir de uno o más clientes como lo vimos en el programa del chat. Para añadir datos usen `open(path_al_archivo, ‘a’)` para agregar datos.
4. El servidor debe poder realizar las siguientes búsquedas y entregarlas a uno o más clientes:
    1. Buscar por nombre y entregar los datos del renglón que se busca:
        1. Ejemplo:
            Cliente: Buscar “Adrián”
            Respuesta del servidor: “Adrián,12345,Masculino,30,ejemplo@.com,SOF25” (Si quieren dar mas formato, son libres de hacerlo)
    2. Aplicar lo mismo para la columna email.
    3. Buscar todos los clientes que cumplan con un criterio de edad.
    4. Buscar todos los clientes que cumplan con un criterio de género.
        Las búsquedas las pueden realizar usando filtros de pandas. Ejemplo: `datos[datos[‘Genero’] == ‘Masculino’]` (esto entrega todos los valores de los datos que cumplen con el género ‘Masculino’).

5. Hagan un menú con las diferentes búsquedas y la opción de añadir datos. Se puede ver de la siguiente manera:
```
Elige una opción
    1. Añadir datos a la base de datos
    2. Buscar por nombre.
    3. Buscar por edad
```
6. Ambos deben de funcionar en diferentes consolas.
7. Los archivos se van a entregar con nombre `db_server_<nombre1nombre2>.py` y `db_client_<nombre1nombre2>.py`.

Tratar de comentar lo más posible. _En caso de que usen ChatGPT_ (que es totalmente válido... pero sí, lo voy a notar) _para generar el código_, entonces también espero que tengan lo siguiente:

8. Manejo concurrente de múltiples clientes (servidor multicliente). Adaptar el servidor para que cada cliente se maneje en un hilo independiente, permitiendo atender a varios clientes al mismo tiempo.
9. Protege el acceso al archivo con Lock. Evitar condiciones de carrera al modificar el archivo CSV desde múltiples hilos.
10. Agregar logs concurrentes. Registrar en un archivo .log las acciones de cada cliente (consultas, inserciones), usando hilos y sincronización.
