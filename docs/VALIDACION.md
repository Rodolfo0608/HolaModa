# Registro de validación

Comprobaciones locales realizadas el 11 de noviembre de 2026 con Python 3.12 en Windows.

| Comprobación | Resultado |
|---|---|
| Suite pytest | 32 pruebas aprobadas |
| Entorno virtual nuevo | Dependencias instaladas desde requirements.txt y 32 pruebas aprobadas sin PYTHONPATH externo |
| Descarga desde cero | Versión 2 descargada y SHA-256 verificado en carpeta temporal |
| Fuente completa | 3.900 registros y monto acumulado USD 233.081 |
| Segunda carga | 3.900 registros, sin acumulación de duplicados |
| Filtro Ropa e Invierno | 448 registros y monto acumulado USD 27.274 |
| Filtros y paginación en navegador | Comprobados en tablero local |
| Swagger | Consulta de resumen ejecutada con respuesta 200 |
| Rollback después de borrar | Prueba automatizada con fallo SQL inducido, instantánea conservada |
| Presentación | Ocho diapositivas renderizadas e inspeccionadas |

Las pruebas automatizadas utilizan muestras pequeñas independientes. Las cifras completas se contrastaron
con el CSV original. Esta validación no equivale a una prueba de carga ni a una auditoría de seguridad.
La ejecución de GitHub Actions se comprueba por separado; el resultado remoto confirmado figura al final.

## Variante Docker

Se incorporaron Dockerfile, Compose, servidor Waitress e instrucciones de traslado de imagen.
Docker no está instalado en este equipo: no se ha construido ni ejecutado el contenedor.
La validación nativa anterior se mantiene separada de esta opción pendiente de prueba.

## Revisión adicional de cumplimiento

El 11 de noviembre de 2026 se repitió la suite: 32 pruebas aprobadas.
El script `scripts/verify_delivery.py` aprobó 42 cotejos del CSV, SQLite y HTTP.
Se incluyen mediciones secuenciales de tres endpoints en `RESULTADO_COTEJO.json`.
La correspondencia de cada requisito está en `MATRIZ_CUMPLIMIENTO.md`.
La comprobación posterior confirmó la publicación del commit 4365e6c y las fuentes y documentos en GitHub.
GitHub Actions completó satisfactoriamente la validación de ese commit:
https://github.com/Rodolfo0608/HolaModa/actions/runs/43130980826
