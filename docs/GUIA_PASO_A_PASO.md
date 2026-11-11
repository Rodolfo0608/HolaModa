# Guía de aprendizaje y ejecución

El proyecto tiene dos momentos: preparar los datos y consultarlos. El ETL prepara una instantánea;
Flask permite consultarla desde una API y el navegador presenta esos resultados.
Conviene ejecutar cada paso y revisar su resultado antes de pasar al siguiente.

## 1 Revisar el entorno

Abrir una terminal en la carpeta del repositorio. Ejecutar `git --version` y `py -3.12 --version`.
Git conserva versiones del código. Python ejecuta los programas. GitHub almacena y comparte el repositorio;
no ejecuta automáticamente el servidor Flask.

## 2 Crear un entorno virtual

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`.venv` separa los paquetes de este proyecto. `requirements.txt` fija las versiones usadas.
No se sube `.venv` a Git: otra persona lo reconstruye con esos comandos.
Las bibliotecas de gráficos y Swagger están dentro de `static/vendor`, con sus licencias.

## 3 Descargar y reconocer la fuente

```powershell
.\.venv\Scripts\python.exe scripts/download_data.py
```

Abrir el CSV solo para reconocer encabezados y primeras filas. No editar el original.
Revisar `data/source.json`: autor, versión, cantidad y SHA-256. Una huella distinta exige revisar qué cambió.
En esta fuente hay una observación por cliente, sin fecha de transacción ni detalle de unidades.

## 4 Ejecutar la carga

```powershell
.\.venv\Scripts\python.exe -m retail.etl
```

Leer `retail/etl.py` en este orden: `REQUIRED`, `transform`, `load` y `main`.
En `transform`, seguir el ejemplo del primer cliente: USD 53 se almacena como 5300 centavos.
`Yes` pasa a 1. `load` valida, reemplaza datos y registra la ejecución.
El mensaje de éxito debe indicar 3.900 filas. Se genera `instance/retail.db`.
Repetir el comando y verificar que el tablero mantiene el mismo número de filas.

## 5 Entender el esquema

Leer `retail/db.py`. `purchases` contiene la muestra actual. `etl_runs` registra cargas satisfactorias.
La clave primaria impide duplicar el identificador del cliente dentro de esa muestra.
La transacción garantiza que borrar e insertar se confirmen juntos o se reviertan juntos.

## 6 Ejecutar las pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Las pruebas utilizan una base temporal; no modifican la demostración.
Estudiar primero `test_summary_matches_known_values`: con 10,10, 20,20 y 30,30, el total es 60,60
y el promedio 20,20. Después revisar la recarga y el rollback por falla de escritura.
Cada prueba comprueba un comportamiento observable, no solo que una función se pueda ejecutar.

## 7 Iniciar Flask y consultar la API

```powershell
.\.venv\Scripts\python.exe app.py
```

Mantener esa terminal abierta. Abrir `/api/health` para comprobar disponibilidad y `/api/summary`
para ver JSON. En `app.py`, seguir `summary`: leer filtros, construir condiciones, consultar SQLite y devolver JSON.
Los valores se pasan como parámetros para que el motor no los interprete como instrucciones SQL.

## 8 Revisar el frontend

Abrir http://127.0.0.1:5000. Revisar `templates/index.html` para reconocer la estructura.
`static/app.css` define la presentación. `static/app.js` consulta los endpoints con `fetch` y actualiza
indicadores, gráficos y tabla. El navegador nunca abre directamente el archivo SQLite.

Seleccionar Ropa e Invierno: 448 registros y USD 27.274. Pasar a la página siguiente del detalle.
Restablecer filtros y comprobar 3.900 registros.

## 9 Probar Swagger

Abrir `/docs`, expandir `GET /api/summary`, pulsar `Try it out`, escribir `Clothing` y `Winter`, y ejecutar.
Observar estado 200 y la respuesta JSON. Probar después `discounted=1`.
La especificación vive en `retail/openapi.py` y se entrega por `/api/openapi.json`.

## 10 Explicar el recorrido completo

Practicar sin leer: «Descargo una versión conocida, valido su estructura y sus valores, cargo una instantánea
transaccional en SQLite y expongo consultas mediante Flask. El navegador consume esa API para presentar
los indicadores. Las pruebas comprueban las reglas de datos y el comportamiento de las consultas».

Explicar con palabras propias por qué se usan centavos, por qué el ETL no corre en cada petición y
por qué el historial de ejecuciones aumenta mientras la cantidad de registros permanece estable.

## 11 Registrar cambios y entregar

```powershell
git status
git diff
git add .
git commit -m "Describe el cambio realizado"
git push origin main
```

Antes de subir, comprobar que no se incluyen CSV originales, bases, `.venv`, contraseñas ni documentos personales.
Revisar la pestaña Actions en GitHub y abrir los enlaces de documentación desde el README.
La instalación completa debe poder repetirse desde otra carpeta.
