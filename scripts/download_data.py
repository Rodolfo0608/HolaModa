"""Descarga la fuente pública y verifica que coincide con la versión revisada."""
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://www.kaggle.com/api/v1/datasets/download/iamsouravbanerjee/customer-shopping-trends-dataset?datasetVersionNumber=2'


def main():
    expected = json.loads((ROOT / 'data/source.json').read_text(encoding='utf-8'))['sha256']
    target = ROOT / 'data/raw/shopping_trends.csv'
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == expected:
        print('La fuente verificada ya está disponible.')
        return
    request = urllib.request.Request(URL, headers={'User-Agent': 'HolaModa-TechnicalTest/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive = response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        content = zipped.read('shopping_trends.csv')
    if hashlib.sha256(content).hexdigest() != expected:
        raise ValueError('La fuente cambió. Revisar la versión antes de cargarla.')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    print(f'Dataset verificado: {target}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'No fue posible descargar los datos: {error}', file=sys.stderr)
        sys.exit(1)
