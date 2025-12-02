# Hito 4: Composición de servicios

## Descripción del hito
En este hito se ha diseñado la infraestructura de despliegue de la aplicación web de Prevención de Ahogamientos utilizando contenedores y composición de servicios. El objetivo principal es ejecutar la aplicación Django y su base de datos PostgreSQL en un clúster reproducible, aislando cada componente en su propio contenedor y definiendo sus relaciones mediante un fichero de composición. De este modo, el entorno de pruebas y despliegue se puede reconstruir de forma idéntica en cualquier máquina que disponga de un motor de contenedores.

## Estructura del clúster de contenedores
El clúster de contenedores definido para este hito tiene como objetivo desplegar la aplicación web de Prevención de Ahogamientos junto con su base de datos de forma aislada y reproducible. Para ello se ha creado un entorno compuesto por varios contenedores que se comunican entre sí, de manera que la lógica de la aplicación y el almacenamiento de datos quedan claramente separados, pero siguen funcionando como un único sistema coherente.

<img width="1288" height="763" alt="image" src="https://github.com/user-attachments/assets/d4d4ac55-c033-4c59-9a33-a62bcb531905" />

En la configuración actual se utilizan dos contenedores principales: el contenedor web y el contenedor de base de datos. El contenedor web ejecuta la aplicación Django, exponiendo el servicio HTTP en el puerto 8000 del host a través del mapeo de puertos definido en Docker Compose. El contenedor db ejecuta un servidor PostgreSQL, configurado con su propia base de datos, usuario y contraseña, y se encarga de almacenar toda la información persistente generada por la aplicación. Ambos contenedores están conectados a la misma red interna de Docker, lo que permite que la aplicación Django se comunique con la base de datos usando el nombre de servicio db como host y el puerto interno 5432.

<img width="1586" height="450" alt="image" src="https://github.com/user-attachments/assets/7e49329c-bd3f-45fa-8303-fd28dc32d875" />

## Configuración de cada contenedor y elección de la imagen base

### Contenedor web

El contenedor web es el encargado de ejecutar la aplicación Django de Prevención de Ahogamientos. Para construirlo se parte de la imagen base python:3.10-slim, una variante oficial de Python basada en Debian reducida en tamaño, pero que mantiene todas las herramientas necesarias para ejecutar aplicaciones en este lenguaje. Esta elección permite disponer de un entorno compatible con Django 5.2 y con librerías adicionales.

<img width="967" height="607" alt="image" src="https://github.com/user-attachments/assets/cb4ae788-89f7-4fcb-b85d-f0d45942b456" />

Sobre esta imagen base se configuran los elementos específicos de la aplicación. En primer lugar se define un directorio de trabajo donde se copiará el código de la aplicación y los ficheros de configuración. A continuación se copian los archivos de dependencias (por ejemplo requirements.txt) y se instalan mediante pip, lo que garantiza que el entorno del contenedor tenga exactamente las mismas bibliotecas que el proyecto.

<img width="1138" height="414" alt="image" src="https://github.com/user-attachments/assets/816e1a1b-d803-431d-92d4-02099665002c" />

Por último, se establece el comando de arranque para que, al iniciar el contenedor, se ejecute directamente el servidor de desarrollo de Django escuchando en el puerto 8000 y atendiendo las peticiones de los usuarios.

### Contenedor db

El contenedor db proporciona el servicio de base de datos PostgreSQL que utiliza la aplicación. Para este propósito se emplea la imagen oficial postgres:16, que incluye un servidor PostgreSQL ya configurado sobre una distribución Linux estable, junto con las herramientas habituales de administración de la base de datos.

<img width="794" height="290" alt="image" src="https://github.com/user-attachments/assets/77f5ffa8-6755-42b3-90ed-cbfdd7d2dd83" />

<img width="492" height="336" alt="image" src="https://github.com/user-attachments/assets/02c55a6c-1f6a-40ac-a5c5-c7cb3b802989" />

La configuración del contenedor se realiza principalmente mediante variables de entorno y volúmenes. Las variables POSTGRES_DB, POSTGRES_USER y POSTGRES_PASSWORD se usan para crear automáticamente la base de datos inicial, el usuario y las credenciales que luego utilizará Django para conectarse.

<img width="1595" height="475" alt="image" src="https://github.com/user-attachments/assets/9656b25d-e1ec-46f4-814f-f9793bac7d93" />

## Documentación del Dockerfile

El Dockerfile del servicio web define paso a paso cómo construir la imagen que ejecuta la aplicación de Prevención de Ahogamientos. La primera instrucción es FROM python:3.10-slim, que selecciona como base una imagen oficial de Python ligera, mantenida por la comunidad y adecuada para ejecutar aplicaciones modernas en este lenguaje. Partir de esta imagen garantiza la presencia del intérprete de Python 3.10, de pip y de la biblioteca estándar. A continuación se establece WORKDIR /app, de modo que todo el código, las dependencias y los comandos posteriores se ejecutan en un directorio aislado dentro del contenedor.

<img width="1092" height="606" alt="image" src="https://github.com/user-attachments/assets/c28c1a69-61f8-4e6b-994c-611b831b0a1f" />

El siguiente bloque del Dockerfile se centra en la instalación reproducible de las dependencias de Python. Para ello se copia primero el fichero requirements.txt al contenedor y se ejecuta pip install -r requirements.txt. De este modo, cualquier máquina que construya la imagen a partir del mismo Dockerfile y del mismo requirements.txt obtendrá el mismo entorno de ejecución. Posteriormente se realiza un COPY . . para copiar el resto del código fuente y archivos estáticos de la aplicación al directorio de trabajo, completando así el contenido de la imagen con todo lo que Django necesita para funcionar. En este punto también se pueden definir variables de entorno (ENV) para ajustar aspectos como el módulo de configuración de Django o el modo de ejecución.

Finalmente, el Dockerfile define el comando de arranque mediante CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"], que indica al contenedor que, cuando se inicie, lance directamente el servidor de desarrollo de Django escuchando en todas las interfaces de red en el puerto 8000. Esta configuración permite que Docker Compose pueda mapear ese puerto al exterior y que la aplicación sea accesible desde el navegador del host. Durante la construcción de la imagen surgieron varios problemas relacionados con bibliotecas científicas como SciPy y con la librería de visualización Bokeh, debido a incompatibilidades entre determinadas versiones de estas dependencias y las versiones de Python usadas. Para resolverlos fue necesario fijar una combinación estable de versiones en requirements.txt y mantener el uso de Python 3.10 en la imagen base, evitando versiones más recientes del intérprete que dejaban de ser compatibles con algunas de las librerías empleadas.

<img width="812" height="248" alt="image" src="https://github.com/user-attachments/assets/097dcb50-8445-4cb6-ba57-389ffbf3cfda" />

## Publicación de imágenes y automatización (GitHub Packages)

En el repositorio del proyecto se incluyen los Dockerfile utilizados para construir las imágenes de los distintos microservicios, situados junto al código fuente de la aplicación. Mantener estos ficheros de construcción bajo control de versiones garantiza que cualquier desarrollador pueda reconstruir exactamente las mismas imágenes en otra máquina, simplemente clonando el repositorio y ejecutando los comandos de construcción correspondientes.

Para la publicación de las imágenes en GitHub Packages se aprovecha el registro de contenedores de GitHub (GHCR). En un escenario manual, el proceso consistiría en autenticarse contra ghcr.io con un token de acceso personal (PAT) generado en GitHub y con permisos sobre el ámbito de packages, construir la imagen con docker buildx build y subirla con docker push usando una etiqueta del estilo ghcr.io/usuario/ProyectoCC-web:latest y estilo ghcr.io/usuario/ProyectoCC-db:latest.

<img width="603" height="317" alt="image" src="https://github.com/user-attachments/assets/933b11fd-e0b2-402d-95ef-f90ced8ed3af" />

<img width="1865" height="855" alt="image" src="https://github.com/user-attachments/assets/375a04a2-1ddd-4c86-b33b-76dc3ebc9451" />

Sin embargo, para automatizar este flujo se ha definido un workflow de GitHub Actions que, en cada push a la rama principal, inicia sesión en GHCR mediante el token automático GITHUB_TOKEN, construye la imagen a partir del Dockerfile del servicio web y la publica en el registro como paquete de tipo container. De esta forma, cada vez que se hace push al repositorio, GitHub Actions ejecuta el workflow, construye las imágenes actualizadas y las sube a GitHub Packages, manteniendo siempre disponible la última versión del clúster de contenedores lista para su despliegue.​

<img width="613" height="266" alt="image" src="https://github.com/user-attachments/assets/23c0a0e8-52ad-4736-8d63-f2503314764e" />

## Documentación del compose.yaml (docker-compose.yml)

El fichero docker-compose.yml describe cómo se ponen en marcha y se conectan los servicios db y web de la aplicación utilizando una sintaxis declarativa en YAML. Cada servicio se define con su imagen, puertos, variables de entorno y volúmenes, de forma que todos los parámetros necesarios para recrear el entorno quedan recogidos en un único archivo de configuración.

En el servicio db se especifica que la imagen a utilizar es la imagen oficial de PostgreSQL en su versión 16. Junto a ella se declaran variables de entorno como POSTGRES_DB, POSTGRES_USER y POSTGRES_PASSWORD, que se usan para crear la base de datos inicial y el usuario con el que se conectará la aplicación. Además se define un mapeo de puertos 5432:5432 para poder acceder al servidor de base de datos desde el host, y un volumen db-data:/var/lib/postgresql/data que persiste los datos en disco incluso si el contenedor se detiene o se vuelve a crear.​

<img width="601" height="346" alt="image" src="https://github.com/user-attachments/assets/3192a656-e369-42ea-a464-081e0b3b0e55" />

El servicio web se construye a partir del código del proyecto usando la directiva build: ., que indica que debe utilizar el Dockerfile situado en el directorio raíz del repositorio. Para garantizar que la base de datos esté disponible antes de arrancar la aplicación, se incluye depends_on: db, de manera que Compose levanta primero el servicio de base de datos y después el contenedor web. El mapeo de puertos 8000:8000 expone el servidor de Django en el puerto 8000 del host, mientras que las variables de entorno del servicio web definen los parámetros de conexión a PostgreSQL.

<img width="838" height="457" alt="image" src="https://github.com/user-attachments/assets/9a80c4d1-c358-4352-9189-2af6d969b599" />

Gracias a ello, levantar el entorno completo se reduce a ejecutar un único comando (docker compose up --build), que construye las imágenes cuando es necesario, arranca ambos servicios en el orden adecuado y deja la aplicación lista para ser utilizada sin necesidad de recordar múltiples comandos individuales.

## Test de validación del clúster




