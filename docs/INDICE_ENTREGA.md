# Índice de entregables y revisión final

## Estado de la entrega

La ejecución nativa fue comprobada y la última suite local aprobó sus 32 casos.
El cotejo de datos dejó 42 comprobaciones aprobadas en `RESULTADO_COTEJO.json`.
La documentación y la presentación están preparadas.

**Publicación comprobada:** el 11 de noviembre de 2026 se verificaron las fuentes y documentos en GitHub,
en el commit `4365e6c`. GitHub Actions completó satisfactoriamente la validación de ese commit.
Resultado: https://github.com/Rodolfo0608/HolaModa/actions/runs/43130980826
Para revisiones posteriores, consultar el estado del commit correspondiente en Actions.

Repositorio de entrega: https://github.com/Rodolfo0608/HolaModa

El enlace al repositorio es lo que permite compartir código, README y documentos. No es una dirección
de la aplicación ejecutándose públicamente. El enunciado no exige alojar la aplicación en internet.

## 1 Código fuente

| Entregable solicitado | Acceso desde el repositorio |
|---|---|
| Código de extracción | [scripts/download_data.py](../scripts/download_data.py) |
| Código de transformación y carga | [retail/etl.py](../retail/etl.py) |
| Esquema y conexión SQLite | [retail/db.py](../retail/db.py) |
| Código de API | [app.py](../app.py) |
| Contrato OpenAPI | [retail/openapi.py](../retail/openapi.py) |
| HTML del frontend | [templates/index.html](../templates/index.html) |
| Lógica del frontend | [static/app.js](../static/app.js) |
| Estilos del frontend | [static/app.css](../static/app.css) |
| Instalación y ejecución | [README.md](../README.md) |
| Dependencias fijadas | [requirements.txt](../requirements.txt) |
| Pruebas automatizadas | [tests](../tests/) |

El repositorio conserva el código y los scripts para reconstruir los datos. El CSV, SQLite y `.venv`
son archivos locales generados, excluidos de Git. Esa exclusión no representa falta de código fuente.

## 2 Documentación técnica

Documento principal: [Diseño técnico de la solución](TECNICO.md).

| Contenido solicitado | Dónde revisarlo |
|---|---|
| Arquitectura | Responsabilidades y modelo en [TECNICO.md](TECNICO.md); diagrama general en [README](../README.md) |
| Decisiones y justificación | Alternativas evaluadas en [TECNICO.md](TECNICO.md); tabla de decisiones en [README](../README.md) |
| Diagrama del flujo de datos | Flujo general en [README](../README.md); validación y transacción en [TECNICO.md](TECNICO.md) |
| Explicación ETL | Proceso y consistencia en [TECNICO.md](TECNICO.md) y explicación del [README](../README.md) |

Documentos de apoyo:

| Documento | Uso |
|---|---|
| [MATRIZ_CUMPLIMIENTO.md](MATRIZ_CUMPLIMIENTO.md) | Cotejo completo de requisitos, criterios, recomendaciones y pendientes |
| [FRONTEND.md](FRONTEND.md) | Herramientas reales, funciones, endpoints y recorrido de una consulta |
| [ARRANQUE_LOCAL.md](ARRANQUE_LOCAL.md) | Ubicación, Flask/Werkzeug, inicio, detención y diagnóstico |
| [VALIDACION.md](VALIDACION.md) | Registro de verificaciones y límites |
| [RESULTADO_COTEJO.json](RESULTADO_COTEJO.json) | Evidencia de 42 verificaciones y mediciones HTTP locales |
| [Origen de los datos](../data/README.md) | Fuente, atribución, descarga y límites de interpretación |

## 3 Presentación técnica

Presentación editable: [Sustentacion_HolaModa_Moderna.pptx](Sustentacion_HolaModa_Moderna.pptx).

| Contenido solicitado | Material de revisión |
|---|---|
| Enfoque utilizado | Diapositivas 1 a 5 |
| Desafíos y soluciones | Proceso de validación, decisiones y notas del PowerPoint |
| Demostración del funcionamiento | Diapositiva 6 y aplicación local |
| Mejoras o escalabilidad | Diapositiva 8 y evolución del documento técnico |

El PowerPoint incluye notas del presentador. El archivo descargado debe abrirse con PowerPoint u otra
aplicación compatible; GitHub puede ofrecer descarga en lugar de previsualización.
La preparación del material no sustituye el ensayo de la explicación y de los comandos.

## Criterios de evaluación

| Criterio | Evidencia y alcance |
|---|---|
| Calidad del código, 30% | Módulos separados, validación, transacciones y errores. Suite de 32 casos unitarios y de integración aprobados localmente |
| Arquitectura y diseño, 25% | Diagrama, separación de carga/consulta/interfaz y justificación de tecnologías en README y documento técnico |
| Funcionalidad, 25% | Flujo completo, filtros y visualizaciones; 42 cotejos y mediciones locales. No hay prueba de carga concurrente ni garantía de rendimiento a gran escala |
| Documentación y presentación, 20% | Documentos y PowerPoint disponibles; explicación oral y respuestas deben practicarse y se evaluarán en la entrevista |

Los porcentajes son los pesos del enunciado, no una calificación obtenida por el proyecto.
El detalle de cada subcriterio y sus límites se encuentra en la matriz de cumplimiento.

## Recomendaciones del enunciado

- Calidad sobre cantidad: alcance acotado a datos, API y visualización reproducible.
- Decisiones documentadas: README y documento técnico.
- Seguridad básica: valores SQL parametrizados, listas de columnas permitidas, inserción de datos con textContent,
  cabeceras de seguridad y servidor nativo escuchando solo en loopback.
- Logging y manejo de errores: consola del ETL y del servidor, errores controlados de API y mensajes en interfaz.
- Ejecución local sencilla: entorno virtual, dependencias fijadas, README y Abrir_tablero.cmd.
- Versionado: historial Git y fuentes publicados; validación remota satisfactoria del commit 4365e6c.
- Docker: alternativa opcional preparada, todavía sin construcción ni ejecución comprobada.

## Enlaces de la demostración local

Requieren levantar el servidor en el equipo desde el cual se abre el navegador:

- Tablero: http://127.0.0.1:5000/
- Swagger: http://127.0.0.1:5000/docs
- Salud: http://127.0.0.1:5000/api/health
- Resumen: http://127.0.0.1:5000/api/summary

No enviar estos enlaces como acceso remoto a la empresa: 127.0.0.1 apunta al propio equipo de quien los abre.

## Última revisión antes de compartir

1. Publicar con `git push origin main` desde la carpeta local del proyecto.
2. Abrir GitHub y confirmar que aparecen app.py, retail, templates, static, tests y docs.
3. Comprobar que el README muestra instrucciones y enlaces y que la presentación se puede descargar.
4. Revisar Actions y verificar el resultado real del último commit publicado.
5. Compartir el enlace principal del repositorio, con indicación de que es una aplicación de ejecución local.
6. Ensayar la demo: 3.900 registros y USD 233.081; Ropa + Invierno: 448 registros y USD 27.274.
