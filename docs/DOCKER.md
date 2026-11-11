# Ejecución opcional con Docker

Esta modalidad empaqueta Python, las dependencias, el código y una muestra ya cargada.
El equipo anfitrión requiere Docker Engine y Compose disponibles. En Windows, Docker Desktop
incluye ambos y debe estar iniciado en modo de contenedores Linux. No requiere instalar Python en el anfitrión.

**Estado de validación:** archivos preparados y revisados. La construcción y ejecución del contenedor
están pendientes de prueba porque Docker no está instalado en el equipo de desarrollo.
La ejecución nativa sí fue comprobada. No presentar la variante Docker como probada hasta completar la lista final.

## Construir y ejecutar

Desde la raíz del repositorio:

```powershell
docker version
docker compose version
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs --tail=50 web
```

La primera construcción necesita internet para obtener la imagen Python, instalar paquetes y descargar
la versión verificada de Kaggle. También ejecuta la suite de pruebas y el ETL: un fallo detiene la construcción.
La etiqueta `python:3.12-slim` puede recibir actualizaciones. Para un despliegue controlado se fijaría
el digest de la imagen base una vez verificada la construcción.

Abrir http://127.0.0.1:5001 y http://127.0.0.1:5001/docs.
El puerto 5001 evita interferir con la ejecución nativa que utiliza el 5000.
El servicio web escucha dentro del contenedor con Waitress y un usuario sin privilegios de root.
El puerto se publica únicamente en el equipo local.

## Datos y persistencia

La imagen contiene el CSV descargado por el script y la base inicial generada durante la construcción.
No se copia el CSV ni la base del equipo de desarrollo. La base activa reside en el volumen `retail_data`.
Al crear ese volumen por primera vez, Docker lo inicializa con el contenido de `/app/instance` de la imagen.
Si el volumen ya existe, mantiene su contenido aunque se reconstruya la imagen.

Para recargar la muestra desde el archivo verificado incluido en la imagen:

```powershell
docker compose exec web python -m retail.etl
```

Ejecutar la recarga antes de iniciar la demostración. Confirmar luego la cantidad y la huella en `/api/pipeline`.
Esta modalidad sigue siendo una demo de consulta local; Docker no incorpora autenticación ni convierte
automáticamente el proyecto en una solución de producción.

## Detener y volver a iniciar

```powershell
docker compose stop
docker compose start
```

`docker compose down` elimina los contenedores y conserva el volumen de datos.
La imagen ya construida puede iniciarse sin conexión usando `docker compose up -d --no-build`.

## Llevar una imagen a otro equipo sin reconstruir

Solo después de construir y probar la imagen en un equipo con Docker:

```powershell
docker image save holamoda-retail:local -o holamoda-imagen.tar
```

Llevar el TAR junto con `compose.yaml`. En el equipo de destino, con Docker iniciado:

```powershell
docker image load -i holamoda-imagen.tar
docker compose up -d --no-build
```

El TAR incluye las capas y los datos iniciales de la imagen; no exporta cambios posteriores del volumen.
Usar un equipo con arquitectura compatible y contenedores Linux. No hay un TAR generado en esta entrega,
porque primero debe comprobarse la construcción. Mantener la distribución y atribución de la fuente
conforme a sus condiciones descritas en `data/README.md`.

## Comprobaciones antes de usarlo en la entrevista

1. La construcción finaliza correctamente.
2. `docker compose ps` muestra el servicio como healthy después de su arranque.
3. El tablero muestra 3.900 registros y USD 233.081.
4. Ropa e Invierno muestra 448 registros y USD 27.274.
5. Swagger ejecuta la misma consulta con respuesta 200.
6. Detener y arrancar conserva el funcionamiento y los datos.
7. Probar el TAR en el equipo de destino si se utiliza el traslado sin internet.

Si el puerto 5001 está ocupado, cambiar únicamente el puerto del anfitrión en `compose.yaml`,
por ejemplo `127.0.0.1:5002:5000`.
Si la fuente no puede descargarse, revisar conectividad y disponibilidad de Kaggle antes de reconstruir.
Si Docker no inicia en el equipo de destino, usar la instalación nativa documentada en el README.

## Referencias

- Instalación de Compose: https://docs.docker.com/compose/install/
- Persistencia de volúmenes: https://docs.docker.com/engine/storage/volumes/
- Ejecución de Waitress: https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html
