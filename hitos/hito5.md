<img width="1483" height="784" alt="image" src="https://github.com/user-attachments/assets/dd6060fb-3db0-44c9-ac26-ce78d7ccaa7b" /># Hito 5: Despliegue de la aplicación en un IaaS o PaaS

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

## Herramientas de observabilidad en el despliegue

Para monitorizar la aplicación en tiempo real se utilizan las herramientas de observabilidad que nos ofrece Railway, que proporcionan en un único panel el consumo actual y estimado del proyecto, junto con los registros detallados de arranque del contenedor, ejecución de migraciones y actividad de la aplicación. Esta información permite detectar rápidamente errores durante el despliegue y controlar el coste y uso de recursos sin necesidad de instalar agentes adicionales.
​
<img width="1593" height="636" alt="image" src="https://github.com/user-attachments/assets/3c40869d-7dfb-441b-87be-bd6b22220185" />

Además del panel de uso global, la plataforma muestra métricas temporales de red, CPU y memoria para el servicio que ejecuta la aplicación, lo que facilita identificar picos de carga durante las pruebas de estrés y comprobar que el contenedor se mantiene dentro de los límites de recursos asignados. Esta combinación de logs en tiempo real y gráficas de rendimiento justifica el uso de las herramientas nativas de Railway como solución de observabilidad, ya que reducen el tiempo de detección de incidencias y permiten correlacionar fácilmente las peticiones enviadas a la aplicación con el comportamiento de la infraestructura subyacente.

<img width="1547" height="495" alt="image" src="https://github.com/user-attachments/assets/8512e47d-4811-45f8-92d3-da42d5b342d2" />

<img width="781" height="495" alt="image" src="https://github.com/user-attachments/assets/2cfb194f-1cb5-4ad2-8095-e8c3ed653fd6" />

## Funcionamiento correcto del despliegue

El despliegue en Railway se considera correcto porque la aplicación Django no solo arranca sin errores, sino que permite navegar por todas las vistas principales, acceder a la base de datos PostgreSQL y ejecutar las mismas operaciones que en el entorno local. Después de cada push a la rama principal, la plataforma reconstruye la imagen Docker, aplica las migraciones y levanta el contenedor sin fallos en los logs, de modo que la aplicación responde con códigos HTTP válidos y muestra los datos esperados, lo que confirma que el entorno en la nube replica el comportamiento del entorno de desarrollo.
​
<img width="1594" height="842" alt="image" src="https://github.com/user-attachments/assets/0919af2f-245c-48d5-934e-7cb8528979a3" />

<img width="1594" height="836" alt="image" src="https://github.com/user-attachments/assets/f7743fd6-974e-4790-b8d4-f6f416b51ac0" />

## Pruebas de prestaciones de la aplicación

Para evaluar las prestaciones de la aplicación desplegada en Railway se ha ejecutado una prueba de carga con ApacheBench, lanzando 200 peticiones concurrentes con un nivel de concurrencia 20 contra la URL pública del servicio en producción. El resultado del test muestra que se completaron las 200 peticiones sin errores, con una media de 42,48 peticiones por segundo, un tiempo medio por petición de 470,755 ms y un tiempo máximo de 700 ms, lo que indica que la aplicación soporta este nivel de carga manteniendo tiempos de respuesta aceptables.

<img width="1483" height="784" alt="image" src="https://github.com/user-attachments/assets/7810eb01-8e03-46e7-9ed1-9f207b6bcc21" />​

Durante la ejecución de la prueba se han monitorizado en Railway las métricas de CPU, memoria y tráfico de red del contenedor, sin observarse un aumento del uso de CPU, mientras que se detecta un pico claro en el network egress coincidente con el envío masivo de respuestas. El consumo de memoria aumenta ligeramente en ese mismo instante, pasando de unos 220 a 240 MB, lo que confirma que la aplicación puede atender ráfagas de peticiones sin degradación significativa del rendimiento ni necesidad de reinicios del servicio.

<img width="763" height="496" alt="image" src="https://github.com/user-attachments/assets/8fa58320-65bb-49f2-803a-4d5392d08a0d" />

<img width="765" height="494" alt="image" src="https://github.com/user-attachments/assets/b1c8f619-7749-45d3-8384-452f7f7e54f8" />

<img width="761" height="477" alt="image" src="https://github.com/user-attachments/assets/046d3d92-58a3-4ab4-9fee-9f6e6fd27b0f" />

## URL de la aplicación desplegada

La aplicación se encuentra desplegada en el entorno de producción del proveedor PaaS, y se expone públicamente en https://prevencion-ahogamientos.up.railway.app/ .
