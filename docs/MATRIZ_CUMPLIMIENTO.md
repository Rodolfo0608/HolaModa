# Cotejo de la prueba técnica con la ejecución nativa

## Conclusión y alcance de la revisión

La implementación nativa cubre el flujo funcional solicitado: extracción de una fuente permitida,
transformación y carga en una base SQL, API REST documentada y aplicación web que consume esa API.
Existen fuentes versionadas localmente, instrucciones de ejecución, documento técnico, diagramas y presentación.

No se debe afirmar que la entrega está cerrada: la revisión remota del 11 de noviembre de 2026 encontró
solo el commit inicial en GitHub. Falta publicar el desarrollo y comprobar la ejecución de Actions.
La capacidad de explicación y las respuestas técnicas requieren ensayo con el candidato y evaluación presencial.
Esta matriz demuestra evidencias de implementación, no garantiza una calificación de la empresa.

Base del cotejo: documento «Prueba Técnica - Analista de Desarrollo e Integración», revisado íntegramente.
Se considera la ejecución nativa en Python 3.12, Flask y Werkzeug, sin Docker.

## Cómo interpretar los estados

- **Verificado:** existe evidencia de código, ejecución o inspección concreta indicada en la fila.
- **Documentado:** existe el material; su claridad y calidad final siguen sujetas a evaluación del lector.
- **Pendiente:** falta una acción necesaria de entrega o una comprobación que no puede darse por hecha.
- **Opcional:** el enunciado lo recomienda o incentiva, sin convertirlo en requisito obligatorio.

## Ingesta y procesamiento de datos

| Punto del documento | Implementación y evidencia | Estado y forma de demostrarlo |
|---|---|---|
| Seleccionar una de las fuentes propuestas | Customer Shopping Trends Dataset de Kaggle, versión 2, shopping_trends.csv; `data/source.json` y `data/README.md` | Verificado. La elección de una fuente satisface el punto; no hay que implementar las cuatro alternativas |
| Extracción de la fuente | `scripts/download_data.py`: descarga HTTPS, extracción del archivo previsto y verificación SHA-256 | Verificado en una descarga desde cero durante la preparación; el cotejo actual confirma la huella local. Repetir la descarga requiere internet |
| Transformaciones necesarias | `retail/etl.py`, función `transform`: tipos, espacios exteriores, booleanos, rangos y centavos monetarios | Verificado por tests y lectura del código. Mostrar USD 53 convertido a 5300 centavos |
| Carga en SQL o NoSQL | SQLite, tabla purchases y auditoría etl_runs; esquema en `retail/db.py` | Verificado. Los identificadores e importes de todas las filas se cotejaron contra el CSV |
| Proceso ETL o ELT | ETL: transformación en Python antes de cargar; carga transaccional de instantánea | Verificado. Reejecución sin duplicados y rollback cubiertos por pruebas |

## API REST

| Punto del documento | Implementación y evidencia | Estado y forma de demostrarlo |
|---|---|---|
| Conexión a base de datos | `connect` en `retail/db.py`; consultas desde `app.py` | Verificado mediante respuestas HTTP sobre la base cargada |
| Endpoints relevantes | Resumen, agrupaciones, filtros, detalle paginado, estado y última carga | Verificado. Ver inventario de rutas en README y Swagger |
| Documentación Swagger/OpenAPI | `/docs` con Swagger UI local y `/api/openapi.json` con contrato 3.0.3 | Verificado: disponible por HTTP y consulta ejecutada desde Swagger durante la revisión manual |
| Buenas prácticas | Consultas parametrizadas, columnas permitidas, validación de parámetros, JSON, códigos HTTP y gestión de errores | Verificado por revisión y tests. No equivale a una auditoría completa de seguridad |

La API es de consulta. El enunciado no exige CRUD ni operaciones POST, PUT o DELETE.
Agregar escrituras solo para mostrar más métodos no es necesario para este caso analítico.

## Frontend

| Punto del documento | Implementación y evidencia | Estado y forma de demostrarlo |
|---|---|---|
| Consumir la API desarrollada | `static/app.js`, funciones api, initialize y refresh; peticiones fetch a `/api/...` | Verificado por código y revisión manual. Mostrar Network/Fetch-XHR y respuesta JSON al cambiar filtros |
| Visualizaciones relevantes | Barras por monto de categoría, dona por cantidad de temporada y top 10 por monto de producto | Verificado manualmente. Agrupaciones completas conciliadas con el CSV por HTTP |
| Interfaz intuitiva | Filtros etiquetados, restablecimiento, indicadores, tablas de valores y detalle paginado | Implementado y revisado manualmente. La intuición de uso es un criterio cualitativo a validar con el usuario |
| Buenas prácticas frontend | Separación HTML/CSS/JS, recursos locales, defer, estados de carga/error, textContent, cancelación de solicitudes y diseño adaptable | Implementado y revisado. Hay medidas de accesibilidad, sin certificación WCAG ni suite automatizada de navegador |

La explicación completa de herramientas, funciones y comunicación con Flask está en `FRONTEND.md`.
Bootstrap, React y jQuery no son dependencias de esta implementación.

## Entregables de código fuente

| Punto del documento | Ubicación | Estado |
|---|---|---|
| Repositorio Git con código ETL | `retail/etl.py`, `scripts/download_data.py` | Verificado localmente. Publicación remota pendiente |
| Código de API | `app.py`, `retail/db.py`, `retail/openapi.py` | Verificado localmente. Publicación remota pendiente |
| Código frontend | `templates/`, `static/app.js`, `static/app.css` y bibliotecas locales | Verificado localmente. Publicación remota pendiente |
| README de instalación y ejecución | `README.md`, comandos nativos desde una carpeta nueva | Documentado y comprobado en entorno virtual nuevo durante la preparación |

La base, el CSV descargado y `.venv` son archivos generados locales excluidos de Git.
Otra persona los reconstruye siguiendo el README. No faltan fuentes por excluir esos archivos.

## Documentación técnica

| Punto del documento | Evidencia | Estado |
|---|---|---|
| Arquitectura de la solución | README y `TECNICO.md`: responsabilidades de descarga, ETL, base, API y navegador | Documentado |
| Decisiones y justificación | Tabla del README y alternativas evaluadas en `TECNICO.md` | Documentado: Flask, SQLite, csv/Decimal, frontend sin compilación y carga completa |
| Diagrama del flujo de datos | Diagrama Mermaid en README y flujo de validación/carga en `TECNICO.md` | Documentado. GitHub renderiza Mermaid; en un editor de texto se verá su código |
| Explicación del ETL | README, `TECNICO.md`, `GUIA_PASO_A_PASO.md` y comentarios de procesos en el código | Documentado y apoyado por tests |

El enunciado permite colocar la documentación en el README. No exige Word o PDF ni un formato específico.

## Presentación técnica

| Punto del documento | Material disponible | Estado y siguiente acción |
|---|---|---|
| Explicar el enfoque | PowerPoint, diapositivas de alcance, arquitectura y decisiones; `SUSTENTACION.md` | Preparado; ensayar con palabras propias |
| Desafíos y soluciones | Guion: límites de la fuente, precisión monetaria, recargas y recursos locales; notas del PowerPoint | Preparado; explicar un ejemplo de cada decisión, sin inventar incidentes |
| Demostración del funcionamiento | Aplicación local y secuencia documentada en `SUSTENTACION.md` | Funcionamiento verificado. Falta que el candidato practique y complete la demostración presencial |
| Mejoras o escalabilidad | Diapositiva final y secciones de evolución en README y documento técnico | Documentado; distinguir posibilidades futuras de funciones ya implementadas |

## Criterios de evaluación y evidencias

| Criterio y peso | Evidencia disponible | Límites de la afirmación |
|---|---|---|
| Calidad del código, 30%: estructura y organización | Módulos separados para ETL, base y contrato; templates, static y tests | La valoración final corresponde al evaluador |
| Calidad del código: buenas prácticas y errores | SQL parametrizado, validaciones, transacciones, errores controlados y logging | Seguridad básica implementada; no se ha realizado una auditoría formal |
| Calidad del código: tests unitarios | 32 casos pytest aprobados de nuevo; transformaciones, API, integración SQLite y rollback | Son pruebas unitarias y de integración. No son 32 pruebas exclusivamente unitarias ni pruebas completas de interfaz |
| Arquitectura y diseño, 25%: diseño | Separación del proceso de carga y consultas; diagramas y modelo de instantánea | No representa todavía una arquitectura distribuida de producción |
| Arquitectura y diseño: elección de tecnologías | Justificación de Flask, SQLite, bibliotecas locales y dependencias contenidas | Debe poder defenderse oralmente |
| Funcionalidad, 25%: requerimientos y datos | Cotejo funcional anterior y 42 comprobaciones adicionales del CSV, SQLite y HTTP | Comprobación sobre la muestra seleccionada, no sobre toda fuente posible |
| Funcionalidad: performance | Medición HTTP local, tres endpoints, diez peticiones secuenciales por endpoint | Sin concurrencia ni millones de filas. El enunciado no fija un SLA; no se garantiza capacidad productiva |
| Documentación y presentación, 20%: claridad y calidad | README, documento técnico, guía, matriz, frontend y PowerPoint | Material preparado; la calidad comunicativa necesita revisión y ensayo |
| Documentación y presentación: explicación y preguntas | Guion y preguntas con respuestas razonadas | Pendiente de práctica del candidato y sustentación presencial |

## Recomendaciones y notas importantes

| Recomendación o nota | Evidencia y estado |
|---|---|
| Calidad sobre cantidad | Alcance acotado al flujo completo, sin funciones ajenas a los datos |
| Documentar decisiones importantes | README y documento técnico |
| Seguridad básica | Validación, SQL parametrizado, cabeceras y escucha solo en loopback; sin login porque no se exige |
| Logging y errores | Logging del ETL y peticiones, excepciones de API en consola y respuestas controladas. No hay plataforma centralizada de logs |
| Fácil ejecución local | `.venv`, requirements fijado, instrucciones y `Abrir_tablero.cmd`; no requiere IIS |
| Docker/contenedores | Opcional, solo incentivado. Archivos preparados y prueba pendiente. No cuenta como comprobación de ejecución nativa |
| Código versionado en Git | Historial local de commits existente. Publicar en GitHub sigue pendiente |
| Documentación en README permitida | Se utiliza README como punto de entrada y docs como ampliación |

## Resultados observados del cotejo nativo

El 11 de noviembre de 2026 se ejecutaron de nuevo las 32 pruebas con resultado satisfactorio.
`scripts/verify_delivery.py` aprobó 42 comprobaciones independientes de lectura:
huella de fuente, correspondencia completa de identificadores e importes, resúmenes, agrupaciones,
16 combinaciones categoría/temporada, detalle, errores y disponibilidad de recursos web.
Los resultados concretos y la hora de ejecución están en `RESULTADO_COTEJO.json`.

| Medición HTTP local | Peticiones secuenciales | Mediana observada | Percentil 95 observado |
|---|---:|---:|---:|
| `/api/summary` | 10 | 12,56 ms | 33,11 ms |
| `/api/groups/category` | 10 | 13,19 ms | 14,29 ms |
| `/api/purchases?per_page=10` | 10 | 12,87 ms | 26,76 ms |

Las mediciones incluyen ida y vuelta HTTP local con urllib y el servidor de desarrollo.
No miden tiempo de dibujado del navegador ni acceso por internet. Dependen del equipo y de su actividad.

## Acciones que faltan antes de enviar o sustentar

1. Publicar los commits locales en `Rodolfo0608/HolaModa`. El remoto consultado aún tenía solo `4ee5159`.
2. Abrir GitHub y comprobar que se ven código, README, documentación y presentación.
3. Revisar el resultado de Actions; no afirmar que pasó si todavía no terminó correctamente.
4. Recorrer el guion con el candidato: arranque, cifras, filtros, Swagger, prueba y decisiones.
5. Confirmar la modalidad de demostración con la empresa y probar el equipo que se llevará.
6. Si se decide mostrar Docker, construir y probar esa variante antes de presentarla como funcional.

No exige la prueba: despliegue público, IIS, React, autenticación, todas las fuentes de datos,
CRUD completo, predicciones, inventario, integración SAP real ni un servidor SQL empresarial.
No convertir esas ampliaciones en supuestos requisitos pendientes.
