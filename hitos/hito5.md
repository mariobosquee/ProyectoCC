# Hito 5: Despliegue de la aplicación en un IaaS o PaaS

## Descripción del hito

Este hito se centra en el despliegue de la aplicación en un proveedor de computación en la nube, configurando tanto la infraestructura necesaria (servicio web y base de datos) como el proceso para que el código pueda publicarse de forma automática desde el repositorio de control de versiones. Además, incorpora mecanismos de observabilidad y pruebas de rendimiento que permiten monitorizar el comportamiento de la aplicación en tiempo real y comprobar que responde correctamente bajo carga en un entorno de producción.

## Criterios de selección de la plataforma en la nube

Para el despliegue en la nube se ha optado por utilizar Railway como plataforma tipo PaaS, ya que permite ejecutar la aplicación Django en contenedores gestionados y ofrecer una base de datos PostgreSQL como servicio sin tener que administrar directamente máquinas virtuales ni sistemas operativos. Además, Railway proporciona integración nativa con GitHub para desplegar automáticamente en cada push, posibilidad de alojar la aplicación en centros de datos europeos y herramientas integradas de logs y métricas básicas que facilitan la supervisión del estado de la aplicación.

<img width="1592" height="722" alt="image" src="https://github.com/user-attachments/assets/18c76ad8-4b01-4eec-91af-dc93dbcbe869" />

Se valoraron alternativas basadas en IaaS clásico y otras plataformas PaaS orientadas a aplicaciones web con PostgreSQL gestionada. Estas opciones ofrecían un mayor control sobre la infraestructura, pero implicaban una complejidad operativa superior o no contaban con despliegues automatizados desde Git y con herramientas de observabilidad.

## Herramientas empleadas para el despliegue en la plataforma PaaS

Para desplegar la aplicación en la plataforma PaaS se han utilizado dos contenedores Docker, el propio sistema de construcción y despliegue continuo del proveedor y el repositorio de GitHub. La imagen de la aplicación Django se define mediante un Dockerfile, lo que permite empaquetar todas las dependencias y ejecutar el mismo contenedor tanto en local como en la nube, mientras que la plataforma se encarga de construir esa imagen a partir del repositorio y lanzar el servicio web en cada nueva versión.

<img width="1592" height="690" alt="image" src="https://github.com/user-attachments/assets/9727e5ca-daad-4004-b6e2-e0d56040a511" />​

El repositorio de GitHub actúa como punto de integración continua. La plataforma se conecta a la rama principal y, cuando se hace un push, dispara automáticamente un nuevo despliegue usando los comandos de arranque ya validados en los hitos anteriores. 

## Configuración del despliegue automático desde GitHub

La aplicación se despliega automáticamente en Railway a partir del repositorio de GitHub, vinculando el proyecto de la plataforma con la rama principal del repositorio (master) y configurando que cada nuevo push dispare una nueva construcción de la imagen y un redepliegue del servicio web. La plataforma reutiliza los mismos comandos definidos para la ejecución en local, de forma que el entorno en la nube replica el comportamiento del entorno de desarrollo sin pasos manuales adicionales.
​
<img width="1591" height="718" alt="image" src="https://github.com/user-attachments/assets/07e09ee0-f36d-455f-9d8a-138069833808" />

La configuración del despliegue se completa definiendo en el panel del proyecto las variables de entorno necesarias para Django y la base de datos, de modo que la misma imagen de contenedor puede desplegarse en distintos entornos simplemente cambiando estos valores. Con este esquema, el flujo de trabajo queda reducido a realizar cambios en el código y hacer push a GitHub.

<img width="1584" height="728" alt="image" src="https://github.com/user-attachments/assets/80e21cd1-029a-4c6b-adfc-ececc67f5843" />









