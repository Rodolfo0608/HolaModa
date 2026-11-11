# Fuente de datos

Customer Shopping Trends Dataset, de Sourav Banerjee:
https://www.kaggle.com/datasets/iamsouravbanerjee/customer-shopping-trends-dataset

Se utiliza `shopping_trends.csv`, versión 2, con 3.900 filas y 19 columnas.
El autor aclara que es una muestra sintética creada para aprendizaje. No son clientes ni operaciones
de Hola Moda. La ubicación corresponde a estados de EE. UU.

La etiqueta de licencia publicada es `Other (specified in description)`. El proyecto referencia la fuente
y descarga el original para ejecución local. No incorpora el CSV al repositorio ni le asigna otra licencia.

## Obtención

Ejecutar `.\.venv\Scripts\python.exe scripts/download_data.py` desde la raíz.
El script solicita la versión 2 por HTTPS, extrae únicamente el archivo esperado y comprueba el SHA-256
contra `source.json`. Si Kaggle exige iniciar sesión, descargar la versión 2 desde su página, colocar
`shopping_trends.csv` en `data/raw/` y repetir el script para verificarlo. No subir credenciales.

## Interpretación

Hay una observación por `Customer ID`; se usa como clave de esta instantánea. No es un modelo general de tickets POS.
`Previous Purchases` es un atributo informado por la fuente, no compras adicionales disponibles en este CSV.
No se suma a los registros ni al monto observado.

`Payment Method` y `Preferred Payment Method` se conservan separados como en el original. La agrupación
`payment` usa el primero. No se interpreta la muestra como evidencia de pagos realmente procesados.

No hay fecha de transacción, cantidad de unidades, costo, inventario ni ticket. No se calculan series
mensuales, margen, unidades vendidas, rotación ni reposición. Los descuentos indican presencia sin
porcentaje ni importe para reconstruir precios anteriores.
