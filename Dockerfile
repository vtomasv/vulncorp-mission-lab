FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS python-base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

FROM python-base AS core
COPY app ./app
COPY data ./data
COPY web ./web
COPY tests ./tests
COPY requirements-legacy.txt ./requirements-legacy.txt
COPY LICENSE NOTICE.md ./
COPY scripts/vendor/anatomy/LICENSE ./licenses/anatomy.txt
RUN mkdir -p /state /secrets && chown 10001:10001 /state /secrets
USER 10001:10001
CMD ["python", "-m", "app.server"]

FROM core AS records
USER root
# Paquetes reales vulnerables para estudiar inventario/aplicabilidad. No se importan.
RUN pip install --no-cache-dir --no-deps --require-hashes --target /opt/legacy -r requirements-legacy.txt
USER 10001:10001
CMD ["python", "-m", "app.targets"]


FROM python-base AS station-os
USER root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server openssh-client curl jq iproute2 dnsutils netcat-openbsd procps less ca-certificates util-linux && rm -rf /var/lib/apt/lists/* \
    && groupadd -g 1000 student && useradd -m -u 1000 -g 1000 -s /bin/bash student && passwd -d student

FROM station-os AS desktop-os
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tigervnc-standalone-server openbox xterm tint2 dbus-x11 novnc websockify fonts-dejavu-core x11-xserver-utils && rm -rf /var/lib/apt/lists/*

FROM station-os AS station-base
COPY app ./app
COPY data ./data
COPY stations ./stations
RUN install -m 755 stations/lab /usr/local/bin/lab && chmod 755 stations/*.sh
ENV LAB_SECRET_DIR=/secrets LAB_STATION=ops
ENTRYPOINT ["/app/stations/entrypoint.sh"]

FROM desktop-os AS desktop
COPY --from=station-base /app /app
COPY --from=station-base /usr/local/bin/lab /usr/local/bin/lab
COPY stations/desk.html /usr/share/novnc/desk.html
ENV LAB_SECRET_DIR=/secrets LAB_STATION=analyst
ENTRYPOINT ["/app/stations/entrypoint.sh"]

FROM station-base AS appdesk
COPY --from=records /opt/legacy /company/records-root/opt/legacy
COPY --from=core /usr/local/lib/python3.12/site-packages /company/mission-root/usr/local/lib/python3.12/site-packages
COPY --from=core /app/app/targets.py /company/active-service/targets.py
COPY --from=anchore/syft:v1.55.0@sha256:4cc92b64ca74ffca4c94d4c8fcc01f217731375300be14d0b6eeb2e82eaa110a /syft /usr/local/bin/syft
COPY --from=anchore/grype:v0.121.0@sha256:621d56d1d68106b787022c81546f7e0a36202a25d1239f0c20195fab8c16f7ea /grype /usr/local/bin/grype
ENV LAB_STATION=appdesk GRYPE_DB_CACHE_DIR=/cache GRYPE_DB_AUTO_UPDATE=false GRYPE_CHECK_FOR_APP_UPDATE=false SYFT_CHECK_FOR_APP_UPDATE=false
