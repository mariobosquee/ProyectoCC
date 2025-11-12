# Hito 3: Diseño e integración de microservicios

## Descripción del hito
En este hito se ha abordado la creación y prueba de un microservicio que expone la funcionalidad principal del backend a través de una API REST desacoplada de la lógica de negocio. Se ha añadido también un sistema de logs, automatización y documentación del diseño por capas.

## Justificación Técnica del Framework

Para implementar el microservicio se ha usado Django REST Framework, seleccionando este framework por su robustez en el diseño de APIs REST en Python, integración nativa con Django, que es el framework en que se esta desarrollando la aplicación, y ecosistema de utilidades para testeo y documentación.

<img width="386" height="225" alt="image" src="https://github.com/user-attachments/assets/1cbbccb8-5679-49f9-a9be-f2f6800b66da" />

## Diseño de la API y Separación en Capas

Cada carpeta tiene una responsabilidad específica, lo que garantiza una alta mantenibilidad y escalabilidad:

  -  Organización de la API: En este microservicio la carpeta api contiene el archivo views.py, donde se define toda la lógica necesaria para procesar las peticiones recibidas a través de los endpoints REST.
En vez de centralizar rutas y lógica en archivos dispersos por la app, se agrupan todas las vistas (funcionalidad API, controladores de endpoints) en este único módulo, logrando:

     - Desacoplamiento: Toda la lógica relativa a la entrada/salida HTTP queda aislada en api/views.py, mientras los modelos y los servicios permanecen fuera.
     - Claridad y mantenibilidad: El desarrollador o el equipo puede identificar rápidamente dónde están las definiciones de cada endpoint REST.
     - Buenas prácticas: La API actúa como puerta de entrada, delegando operaciones complejas hacia servicios o utilidades especializadas cuando es necesario.

<img width="962" height="459" alt="image" src="https://github.com/user-attachments/assets/f8355cfc-fdcc-4356-ba72-1109fdc5bfae" />

  -  Lógica de negocio en la carpeta services: La carpeta services está dedicada a almacenar funciones y módulos reutilizables que resuelven la lógica de negocio central de la aplicación. Dos archivos componen esta carpeta:

     - graficas.py: Este módulo engloba las funciones responsables de la generación y procesamiento de datos para el análisis y visualización gráfica y demás consultas. Permite construir visualizaciones complejas a partir de los datos del modelo, sirviendo tanto a la API como otros scripts o componentes internos, sin repetir código.
     - utils.py: Aquí residen funciones auxiliares, helpers o utilidades genéricas necesarias para diversas operaciones dentro del microservicio. Puede incluir funciones para la validación de datos, formateo, manejo de fechas, procesamiento de strings y otras tareas comunes transversales a varios módulos.

<img width="1054" height="582" alt="image" src="https://github.com/user-attachments/assets/04f251c8-c3bc-47e7-8a33-fda83a872a44" />

  -  Carpeta test y pruebas automatizadas: La carpeta test está destinada a almacenar todos los archivos para pruebas unitarias y de integración del microservicio. Se han implementado tres nuevas pruebas automáticas para la API REST, verificando el correcto funcionamiento de generar_grafica_lineas, generar_mapa y generar_kmeans.
    
<img width="776" height="453" alt="image" src="https://github.com/user-attachments/assets/1be1c9f4-4983-42b9-8729-391b38067ee7" />

<img width="1890" height="541" alt="image" src="https://github.com/user-attachments/assets/f5a48d58-893c-42c0-951b-bb58576ab409" />

<img width="1357" height="809" alt="image" src="https://github.com/user-attachments/assets/f9fad314-cf9d-4609-8656-63f4f8533f96" />

  -  Directorio raíz del proyecto: En la raíz del proyecto se encuentran los archivos principales del núcleo de la aplicación Django, indispensables para su correcto funcionamiento y organización. admin.py define la configuración y administración de los modelos en el panel de Django. Por su parte, apps.py gestiona la configuración de la app, sirviendo como punto de entrada para parámetros importantes. El archivo models.py registra todas las entidades y relaciones de la base de datos mediante el ORM, y urls.py centraliza la definición de rutas públicas del proyecto, enlazando cada URL con la vista correspondiente.

<img width="199" height="386" alt="image" src="https://github.com/user-attachments/assets/beec7745-93e2-47a8-95bf-41300e248b56" />

## Sistemas de logs

La API implementa un sistema de registro de actividad donde cada evento relevante se almacena y queda disponible tanto en consola como en ficheros mediante la configuración estándar de la librería logging de Python. El sistema utiliza dos handlers: uno para mostrar los mensajes directamente en la consola, facilitando la monitorización en tiempo real durante el desarrollo o despliegue, y otro que guarda los logs en el archivo logs/myapp.log, permitiendo hacer seguimiento y auditoría del comportamiento de la aplicación en producción. Todos los registros se gestionan a nivel raíz y con nivel de detalle INFO, lo que asegura que se capturan tanto eventos informativos como advertencias y errores, manteniendo la trazabilidad y facilitando futuras tareas de mantenimiento o debugging.

<img width="486" height="450" alt="image" src="https://github.com/user-attachments/assets/aff454a8-6b9e-4532-ad1f-8f4d1f6c9bb4" />

<img width="1475" height="342" alt="image" src="https://github.com/user-attachments/assets/b408aa48-6890-4463-81b9-d590a9c8e218" />
