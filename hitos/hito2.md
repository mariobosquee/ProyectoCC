# Hito 2: Integración continua

En este hito se ha llevado a cabo el desarrollo de unos test para verificar el correcto funcionamiento de la aplicación. Además, con el objetivo 
de tener una integración continua del proyecto, se usará GitHub Actions para poder pasar los test automáticamente.

## Desarrollo de los test

Estos tests prueban las funcionalidades de generación de gráficos en mi aplicación web desarrollada con Django, asegurando que el servidor responde 
correctamente bajo diferentes condiciones de entrada. Los test

En el grupo de TestGenerarGraficaApilada, se verifica primero que al enviar una petición POST con parámetros válidos como comunidad, año, color por 
sexo y opción de incluir solo incidentes mortales, el servidor devuelve un JSON con la clave grafica_html, que indica que la gráfica se generó correctamente. 
También se comprueba la gestión de errores cuando faltan campos obligatorios por rellenar, cuando no se envía ninguna comunidad o provincia y no se 
proporciona el año, la respuesta JSON contiene un error.

En el grupo de TestGenerarGraficaCircular, los tests validan que al enviar nacionalidades y un rango de años en la petición, la vista devuelve exitosamente 
la gráfica circular con la clave grafica_html en la respuesta JSON. Además, se verifica que si no se proporciona ninguna nacionalidad, el sistema responde 
adecuadamente con un error en el JSON.

Por último, en el grupo de TestGenerarGraficaLineas, se confirma que al enviar un año válido y la opción sobre incluir solo muertos, la aplicación genera 
la gráfica de líneas correcta y la devuelve en la respuesta. También se asegura que el sistema gestione el error de entrada cuando no se proporciona un año.

## Vincular test con GitHub Actions (integración continua)

Para conectar el proyecto Django con GitHub Actions y habilitar la integración continua, se aprovechó la plantilla automática que GitHub ofrece para proyectos Django. Al crear el fichero django.yml﻿ en la carpeta .github/workflows/﻿, GitHub generó una estructura base para ejecutar tests en el proyecto. Solo fue necesario indicar la versión de Python utilizada, lo que facilitó la configuración inicial sin tener que escribir el flujo completo desde cero.

Además, para que los tests y el entorno de GitHub Actions funcionaran correctamente con las dependencias del proyecto, se generó el archivo requirements.txt﻿. Este documento contiene todas las librerías usadas y sus versiones exactas, permitiendo que el runner de GitHub Actions instale el entorno idéntico al de desarrollo. Para crear este archivo, se ejecutó el comando pip freeze > requirements.txt﻿ desde el terminal de Visual Studio Code, lo que volcó automáticamente la lista de paquetes instalados en el entorno virtual en el fichero.

Con estos pasos, se logró configurar un pipeline de integración continua que automáticamente instala las dependencias, ejecuta las pruebas del proyecto Django y notifica del estado, ayudando a mantener la calidad del código y detectar errores con rapidez cada vez que se hace push al repositorio.
