# Guion de sustentación

Duración propuesta: 10 a 12 minutos, seguida de preguntas. Practicar el texto con palabras propias
y ajustar cualquier afirmación a lo que efectivamente se haya revisado y ejecutado.

## Apertura de un minuto

«Elegí un análisis de tendencias de compra por su relación con retail y con mi experiencia en integración
de sistemas. El objetivo fue construir el recorrido completo del dato, con validaciones y una ejecución
local sencilla. La fuente es sintética y no representa información de Hola Moda».

## Arquitectura de dos minutos

Mostrar el diagrama del README. Explicar la separación del ETL, la base, la API y el navegador.
Flask sirve las páginas y el JSON. JavaScript consume la API. SQLite conserva la muestra.
La descarga y la carga ocurren antes de la consulta; no dependen de una petición del usuario.

## Proceso de datos de dos minutos

Mostrar `transform` y el bloque transaccional de `load`. Explicar las validaciones y la conversión a centavos.
Repetir una carga y confirmar que no se acumulan registros. Mostrar la huella y el historial.
Si preguntan por datos inválidos, explicar que se rechaza el lote y se conserva la última carga válida.

## Demostración de tres minutos

1. Abrir el tablero sin filtros y reconocer sus 3.900 registros y USD 233.081.
2. Seleccionar Ropa e Invierno: 448 registros y USD 27.274. Cambiar de página y restablecer.
3. Abrir Swagger y consultar `/api/summary` con `category=Clothing` y `season=Winter`.
4. Mostrar JSON y código 200. Explicar que son los mismos datos que usa el tablero.
5. Ejecutar `python -m pytest -q` utilizando el intérprete de `.venv`.

Mantener el servidor abierto en una terminal y usar otra para ETL y pruebas. Ejecutar las cargas antes
de consultar las cifras. Llevar el proyecto preparado y los recursos locales para no depender del Wi-Fi.

## Desafíos y soluciones de dos minutos

- La fuente no contiene fechas ni tickets. Se definieron métricas descriptivas de una instantánea.
- Los importes requieren precisión. Se conservaron como centavos enteros.
- Una recarga puede generar duplicados. Se implementó reemplazo transaccional.
- La demostración podría depender de internet. Gráficos y Swagger usan archivos locales.

Presentar estos puntos como problemas concretos abordados en el proyecto. No afirmar mejoras de rendimiento
o resultados comerciales que no se hayan medido.

## Preguntas para practicar

**¿Por qué Flask?** Ya forma parte de mi experiencia y permite exponer la API y servir una interfaz sencilla
sin otra cadena de herramientas. Mantengo separados transformación, esquema y contrato.

**¿Por qué SQLite?** Reduce la instalación para una muestra pequeña. Para más escritores o uso compartido
evaluaría PostgreSQL, migraciones y pruebas de carga.

**¿Esto es ETL o ELT?** ETL: valido y transformo en Python antes de cargar SQLite. Las agregaciones de consulta
se calculan luego en SQL.

**¿Qué significa idempotencia aquí?** La instantánea mantiene los mismos registros y cifras al repetir el archivo.
El registro de ejecuciones sí añade una entrada nueva deliberadamente.

**¿Por qué no se usa Customer ID como ticket real?** Solo identifica la observación de esta fuente. Un POS real
necesitaría claves de ticket y detalle, además del cliente.

**¿Qué pasa si falla después de borrar?** El borrado y la inserción están en una misma transacción.
Una falla de escritura revierte el cambio; hay una prueba con un trigger que provoca ese fallo.

**¿Se calcula rotación o reposición?** No hay inventario ni unidades para hacerlo. Haría falta otra fuente
y reglas de negocio validadas.

**¿Se exponen los errores SQL?** El servidor los registra y entrega un error controlado al cliente.
Los valores del filtro van como parámetros y las columnas se limitan a opciones permitidas.

**¿Por qué no Docker?** El enunciado lo incentiva. Se priorizó una ejecución local comprobada con entorno virtual
y dependencias fijadas. Contenedores serían una mejora posterior, probada antes de presentarla.

**¿Qué mejorarías primero?** Depende del uso: para operación compartida, acceso por roles y PostgreSQL;
para más datos, staging y procesamiento por lotes; para integración continua de POS, claves y carga incremental.

**¿Usaste herramientas de apoyo?** Si lo preguntan, describir de forma honesta el apoyo utilizado y demostrar
la revisión y comprensión del código. Poder explicar y modificar el comportamiento es parte de la sustentación.

## Antes de salir a la entrevista

Confirmar arranque local, descarga ya resuelta, tests, acceso al repositorio, copia de respaldo y apertura
de la presentación. Probar la demostración en el equipo que se llevará. Verificar conexión del proyector
y tamaño del navegador para que las cifras sean legibles.
