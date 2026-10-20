FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS core
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app ./app
COPY data ./data
COPY web ./web
COPY tests ./tests
COPY requirements-legacy.txt ./requirements-legacy.txt
COPY LICENSE NOTICE.md ./
COPY scripts/vendor/anatomy/LICENSE ./licenses/anatomy.txt
RUN mkdir -p /state && chown 10001:10001 /state
USER 10001:10001
CMD ["python", "-m", "app.server"]

FROM core AS records
USER root
# Paquetes reales vulnerables para estudiar inventario/aplicabilidad. No se importan.
RUN pip install --no-cache-dir --no-deps --require-hashes --target /opt/legacy -r requirements-legacy.txt
USER 10001:10001
CMD ["python", "-m", "app.targets"]
