#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
dc(){ docker compose "$@"; }
need(){ command -v docker >/dev/null || { echo 'Instala Docker Engine/Compose o Docker Desktop. Ver docs/INICIO.md.'; exit 1; }; docker info >/dev/null 2>&1 || { echo 'Abre Docker y espera a que el motor esté listo.'; exit 1; }; }
usage(){ cat <<'TXT'
VulnCorp Mission Lab · sin herramientas de seguridad instaladas en el host
  ./lab.sh doctor                    comprobar el equipo
  ./lab.sh up                        construir e iniciar los puestos
  ./lab.sh prepare-game              preparar puestos, base Grype e IA (Internet)
  ./lab.sh ssh                       entrar por llave desde tu terminal
  ./lab.sh down                      detener solo este proyecto; conserva evidencia
  ./lab.sh discover public|support    observar rutas desde una zona
  ./lab.sh probe public export        prueba acotada (transaction/diagnostics/backup)
  ./lab.sh sbom                      Syft real sobre imágenes exportadas
  ./lab.sh scan                      Grype real; primera vez descarga su base
  ./lab.sh ai-prepare                 descargar motor y modelo (Internet)
  ./lab.sh ai-on                      iniciar IA aislada; puestos siguen activos
  ./lab.sh ai-off                     liberar RAM de IA; conserva puestos y controles
  ./lab.sh webscan-on                iniciar ZAP interno (solo cuando se usa)
  ./lab.sh webscan-off               detener ZAP y liberar memoria
  ./lab.sh test                       pruebas unitarias en Docker
  ./lab.sh smoke                      pruebas integradas contra el entorno
  ./lab.sh export                     guardar expediente en artifacts/
  ./lab.sh status                     estado y límites del proyecto
  ./lab.sh reset-targets              volver a fallas iniciales; conserva bitácora
TXT
}
cmd=${1:-help}
if [[ "$cmd" == help ]]; then usage; exit 0; fi
need
mkdir -p artifacts/images
case "$cmd" in
 doctor)
  docker version --format 'Motor: {{.Server.Version}} / {{.Server.Os}} / {{.Server.Arch}}'
  docker info --format 'Memoria asignada a Docker (bytes): {{.MemTotal}}'
  docker compose version
  echo 'Referencia: equipo de 16 GB, Docker con 8 GB, 2 CPU para IA; 40 GB de disco libre mínimo recomendado.'
  echo 'El caso funciona sin GPU. Primera preparación requiere Internet; después se usan cachés.';;
 up) dc build mission records workstation ops appdesk; dc up -d --wait mission records gateway backup validation collector workstation ops appdesk; if [[ "${LAB_SKIP_AI:-0}" != 1 ]]; then dc --profile ai up -d --wait ollama; fi; echo 'Abre http://localhost:8095 (o el LAB_PORT de .env).';;
 prepare-game)
  ./lab.sh up
  dc run --rm --no-deps grype db update
  dc run --rm --no-deps prepare-cache
  ./lab.sh ai-prepare
  ./lab.sh webscan-on
  echo 'Campaña preparada. Abre http://localhost:8095 y entra al puesto.';;
 ssh)
  command -v ssh >/dev/null || { echo 'Instala o habilita el cliente OpenSSH de tu equipo.'; exit 1; }
  mkdir -p artifacts/ssh
  chmod 700 artifacts/ssh
  cp training/ssh/vulncorp_student_ed25519 artifacts/ssh/student_ed25519
  chmod 600 artifacts/ssh/student_ed25519
  endpoint=$(dc port mission 2222)
  [[ "$endpoint" == 127.0.0.1:* ]] || { echo 'SSH debe estar publicado solo en 127.0.0.1. Ejecuta up y revisa Compose.'; exit 1; }
  ssh_port=${endpoint##*:}
  # Trust the host PUBLIC key read from our own container, never disable host verification.
  host_public_key=$(dc exec -T workstation cat /journal/host_ed25519.pub </dev/null)
  printf '%s %s\n' "[127.0.0.1]:$ssh_port" "$host_public_key" > artifacts/ssh/known_hosts
  chmod 600 artifacts/ssh/known_hosts
  shift
  exec ssh -i artifacts/ssh/student_ed25519 -p "$ssh_port" -o IdentitiesOnly=yes -o ForwardAgent=no -o StrictHostKeyChecking=yes -o UserKnownHostsFile=artifacts/ssh/known_hosts student@127.0.0.1 "$@";;
 down) dc --profile ai --profile tools --profile scanners --profile webscan down;;
 status) dc --profile ai ps; ids=$(dc ps -q); if [[ -n "$ids" ]]; then docker stats --no-stream $ids; fi;;
 discover|probe)
  zone=${2:-public}; [[ "$zone" == public || "$zone" == support ]] || { echo 'Zona: public o support'; exit 1; }
  if [[ "$cmd" == discover ]]; then dc run --rm --no-deps "probe-$zone" discover
  else action=${3:-transaction};dc run --rm --no-deps "probe-$zone" probe "$action";fi;;
 sbom)
  docker image inspect vulncorp-records:0.1.0 >/dev/null
  docker image save vulncorp-records:0.1.0 -o artifacts/images/records.tar
  docker image save vulncorp-core:0.1.0 -o artifacts/images/mission.tar
  dc run --rm --no-deps syft docker-archive:/input/records.tar -o cyclonedx-json > artifacts/sbom-records.cdx.json
  dc run --rm --no-deps syft docker-archive:/input/mission.tar -o cyclonedx-json > artifacts/sbom-mission.cdx.json
  dc run --rm --no-deps syft version > artifacts/syft-version.txt
  echo 'SBOMs reales: artifacts/sbom-records.cdx.json y sbom-mission.cdx.json';;
 scan)
  [[ -s artifacts/sbom-records.cdx.json ]] || { echo 'Ejecuta primero ./lab.sh sbom';exit 1; }
  dc run --rm --no-deps grype sbom:/reports/sbom-records.cdx.json -o json > artifacts/grype-records.json
  dc run --rm --no-deps grype db status > artifacts/grype-db-status.txt
  echo 'Reporte real: artifacts/grype-records.json. El juego ejecuta su propio escaneo desde aplicaciones; este reporte completo es una extensión docente.';;
 ai-prepare)
  dc -f compose.yaml -f compose.preload.yaml --profile ai up -d --wait ollama
  trap 'dc --profile ai up -d --wait --force-recreate ollama' EXIT
  dc exec -T ollama ollama pull "${OLLAMA_MODEL:-qwen3:1.7b}"
  # Recrear con el archivo base quita la única red temporal con egreso.
  dc --profile ai up -d --wait --force-recreate ollama
  trap - EXIT
  echo 'Pesos descargados; Ollama volvió a la red interna. Ejecuta ./lab.sh ai-on.';;
 ai-on)
  dc --profile ai up -d --wait mission ollama
  echo 'IA local CPU lista. Puestos y servicios siguen activos.';;
 ai-off)
  dc --profile ai stop ollama
  echo 'IA detenida y memoria liberada. Puestos, servicios y medidas permanecen activos.';;
 webscan-on) dc --profile webscan up -d --wait webscan;;
 webscan-off) dc --profile webscan stop webscan;;
 test) dc run --rm --no-deps check;;
 smoke) dc exec -T mission python -m tests.smoke;;
 export) dc exec -T mission python -c 'import json; from app.server import export_bundle; print(json.dumps(export_bundle(),ensure_ascii=False,indent=2))' > artifacts/expediente.json; echo 'Guardado: artifacts/expediente.json';;
 reset-targets) dc restart gateway records backup; echo 'Targets reiniciados. Se conservan evidencias y decisiones históricas.';;
 *) usage;exit 1;;
esac
