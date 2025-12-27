# Hito 5: Despliegue de la aplicación en un IaaS o PaaS

## Descripción del hito

Este hito se centra en el despliegue de la aplicación en un proveedor de computación en la nube, configurando tanto la infraestructura necesaria (servicio web y base de datos) como el proceso para que el código pueda publicarse de forma automática desde el repositorio de control de versiones. Además, incorpora mecanismos de observabilidad y pruebas de rendimiento que permiten monitorizar el comportamiento de la aplicación en tiempo real y comprobar que responde correctamente bajo carga en un entorno de producción.

## Criterios de selección de la plataforma en la nube

Para el despliegue en la nube se ha optado por utilizar Railway como plataforma tipo PaaS, ya que permite ejecutar la aplicación Django en contenedores gestionados y ofrecer una base de datos PostgreSQL como servicio sin tener que administrar directamente máquinas virtuales ni sistemas operativos. Además, Railway proporciona integración nativa con GitHub para desplegar automáticamente en cada push, posibilidad de alojar la aplicación en centros de datos europeos y herramientas integradas de logs y métricas básicas que facilitan la supervisión del estado de la aplicación.

<img width="1598" height="768" alt="image" src="https://github.com/user-attachments/assets/83d60fad-096c-4f62-8f51-d4fdd7ca6d19" />

Se valoraron alternativas basadas en IaaS clásico y otras plataformas PaaS orientadas a aplicaciones web con PostgreSQL gestionada. Estas opciones ofrecían un mayor control sobre la infraestructura, pero implicaban una complejidad operativa superior o no contaban con despliegues automatizados desde Git y con herramientas de observabilidad.

## Herramientas empleadas para el despliegue en la plataforma PaaS

Para desplegar la aplicación en la plataforma PaaS se han utilizado dos contenedores Docker, el propio sistema de construcción y despliegue continuo del proveedor y el repositorio de GitHub. La imagen de la aplicación Django se define mediante un Dockerfile, lo que permite empaquetar todas las dependencias y ejecutar el mismo contenedor tanto en local como en la nube, mientras que la plataforma se encarga de construir esa imagen a partir del repositorio y lanzar el servicio web en cada nueva versión.
​
El repositorio de GitHub actúa como punto de integración continua. La plataforma se conecta a la rama principal y, cuando se hace un push, dispara automáticamente un nuevo despliegue usando los comandos de arranque ya validados en los hitos anteriores. Además, el panel de configuración del proveedor permite definir las variables de entorno necesarias (parámetros de Django y credenciales de PostgreSQL) y asociar servicios gestionados como la base de datos, por lo que toda la infraestructura queda descrita de forma declarativa y puede reproducirse fácilmente en otra cuenta o región.










