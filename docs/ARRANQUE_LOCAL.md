# Ubicación y arranque del proyecto sin Docker

## Carpeta de trabajo actual

```text
C:\Users\braya\Documents\Codex\2026-11-11\tengo-que-realizar-esta-prueba-t\outputs\HolaModa
```

Pegar esa ruta en la barra de direcciones del Explorador de archivos.
La carpeta contiene el repositorio local, sus fuentes, documentos, entorno virtual y datos de demostración.
El ZIP `HolaModa-entrega.zip` está en la carpeta `outputs`, un nivel por encima.
Ese ZIP es una copia para entrega; no contiene `.venv`, el CSV original ni la base generada.

## Qué servidor utiliza

Flask es el framework Python que recibe peticiones y define las rutas de la aplicación.
Al ejecutar `app.py`, su llamada a `create_app().run(...)` inicia el servidor de desarrollo Werkzeug.
No interviene IIS y no hace falta configurarlo para esta demostración.

`127.0.0.1` es la dirección de la propia computadora, también conocida como loopback.
`5000` es el puerto donde escucha este proceso. La dirección completa es `http://127.0.0.1:5000`.
La misma dirección en otra computadora apunta a esa otra computadora, no a la laptop de desarrollo.
La configuración actual solo permite acceso desde el propio equipo.

Flask sirve tanto las páginas y archivos estáticos como la API. Son funciones distintas dentro del mismo proceso.
SQLite es un archivo consultado por Python, no un servicio de Windows independiente.
El servidor de desarrollo es adecuado para esta demo local; un despliegue operativo requiere un servidor WSGI
y los controles correspondientes. La alternativa Docker prepara Waitress, pero sigue pendiente de prueba.

## Arrancar en este equipo

Forma sencilla: abrir `Abrir_tablero.cmd` mediante doble clic desde la carpeta del proyecto.
Ese archivo cambia a su propia carpeta y ejecuta el Python del entorno virtual. Mantener la ventana abierta.

Forma explícita en PowerShell:

```powershell
cd "C:\Users\braya\Documents\Codex\2026-11-11\tengo-que-realizar-esta-prueba-t\outputs\HolaModa"
.\.venv\Scripts\python.exe app.py
```

El mensaje esperado incluye `Running on http://127.0.0.1:5000` y `Debug mode: off`.
La advertencia de Flask sobre producción describe el uso previsto del servidor; no significa que el arranque haya fallado.

Abrir en el navegador:

| Dirección | Qué permite comprobar |
|---|---|
| http://127.0.0.1:5000/ | Tablero |
| http://127.0.0.1:5000/docs | Swagger interactivo |
| http://127.0.0.1:5000/api/health | Debe devolver status ok y rows 3900 |
| http://127.0.0.1:5000/api/summary | Indicadores sin filtros |

No es necesario volver a descargar ni cargar los datos cada vez que se inicia el servidor.
La base `instance/retail.db` permanece al cerrar el proceso.

## Detener y reiniciar

Presionar `Ctrl+C` en la terminal que ejecuta Flask. Para arrancar otra vez, repetir el comando.
Si se modifica código Python, detener y volver a ejecutar: el recargador automático está desactivado.
Si se modifica CSS o JavaScript, recargar el navegador; usar `Ctrl+F5` si parece conservar una versión anterior.

Si la aplicación ya responde en el puerto 5000, reutilizar esa instancia o detenerla desde su terminal.
No es necesario iniciar una segunda. Si el puerto lo utiliza otra aplicación, puede elegirse temporalmente otro:

```powershell
.\.venv\Scripts\python.exe -m flask --app app:create_app run --host 127.0.0.1 --port 5002
```

En ese caso abrir `http://127.0.0.1:5002`.

## Comprobar pruebas y datos

Abrir una segunda terminal en la misma carpeta, manteniendo la terminal del servidor abierta:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/verify_delivery.py
```

El primer comando no necesita servidor y utiliza bases temporales.
El segundo requiere el servidor en ejecución, coteja el CSV con SQLite y la API y escribe `docs/RESULTADO_COTEJO.json`.
No modifica los datos de la aplicación. Para otro puerto, añadir `--base-url http://127.0.0.1:5002`.

Si la base falta o devuelve 503, ejecutar `.\.venv\Scripts\python.exe -m retail.etl` y volver a consultar.
Si falta el CSV, ejecutar primero `scripts/download_data.py` con el mismo intérprete.

## Preparación de otro equipo

Seguir la instalación del README: instalar Python 3.12, crear su propio entorno virtual, instalar dependencias,
descargar la fuente verificada y ejecutar el ETL. No copiar `.venv` como si fuera una aplicación portátil.
La URL local funciona solo después de levantar el servidor en ese equipo.

Referencia del servidor: https://flask.palletsprojects.com/en/stable/server/
