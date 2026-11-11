FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt requirements-docker.txt ./
RUN python -m pip install --no-cache-dir -r requirements-docker.txt

COPY app.py pytest.ini ./
COPY retail/ retail/
COPY scripts/ scripts/
COPY templates/ templates/
COPY static/ static/
COPY data/source.json data/source.json
COPY tests/ tests/

# La imagen se prepara con datos verificados para no descargar durante la demo.
RUN python -m pytest -q \
    && python scripts/download_data.py \
    && python -m retail.etl \
    && groupadd --gid 10001 retail \
    && useradd --uid 10001 --gid retail --no-create-home retail \
    && chown -R retail:retail /app

USER retail
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/health', timeout=3)"

CMD ["waitress-serve", "--listen=0.0.0.0:5000", "--call", "app:create_app"]
