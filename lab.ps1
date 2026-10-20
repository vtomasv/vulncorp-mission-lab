param(
  [string]$Command = 'help',
  [string]$Zone = 'public',
  [string]$Action = 'transaction'
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function DC { & docker compose @args; if ($LASTEXITCODE -ne 0) { throw 'Docker Compose no pudo completar el paso. Revisa docs/SOLUCIONES.md.' } }
function Write-Utf8($Path, $Lines) { [IO.File]::WriteAllText((Join-Path $PSScriptRoot $Path), ($Lines -join "`n"), (New-Object System.Text.UTF8Encoding($false))) }
if ($Command -eq 'help') {
  Write-Host '.\lab.ps1 up | prepare-game | ssh | doctor | status | down | sbom | scan | ai-prepare | ai-on | ai-off | test | smoke | export | reset-targets'
  Write-Host '.\lab.ps1 discover public     .\lab.ps1 discover support'
  Write-Host '.\lab.ps1 probe public export     .\lab.ps1 probe public transaction'
  return
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Instala Docker Desktop con backend Linux. Ver docs/INICIO.md.' }
& docker info *> $null
if ($LASTEXITCODE -ne 0) { throw 'Abre Docker Desktop y espera a que el motor termine de iniciar.' }
New-Item -ItemType Directory -Force artifacts/images | Out-Null
switch ($Command) {
  doctor { docker version --format 'Motor: {{.Server.Version}} / {{.Server.Os}} / {{.Server.Arch}}'; docker info --format 'RAM Docker (bytes): {{.MemTotal}}'; DC version; Write-Host 'Referencia: 16 GB RAM, Docker 8 GB, CPU sin GPU. Ver docs/INICIO.md.' }
  up { DC build mission records workstation ops appdesk; DC up -d --wait mission records gateway backup workstation ops appdesk; if ($env:LAB_SKIP_AI -ne '1') { DC --profile ai up -d --wait ollama }; Write-Host 'Abre http://localhost:8095 (o LAB_PORT de .env).' }
  prepare-game { & $PSCommandPath up; DC run --rm --no-deps grype db update; DC run --rm --no-deps prepare-cache; & $PSCommandPath ai-prepare; Write-Host 'Campaña preparada. Abre http://localhost:8095.' }
  ssh {
    if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) { throw 'Habilita el cliente OpenSSH de Windows.' }
    New-Item -ItemType Directory -Force artifacts/ssh | Out-Null
    $KeyPath = Join-Path $PSScriptRoot 'artifacts/ssh/student_ed25519'
    # Repeated connections must also work after the prior copy was made read-only for this user.
    if (Test-Path $KeyPath) { Remove-Item -Force $KeyPath }
    Copy-Item 'training/ssh/vulncorp_student_ed25519' $KeyPath
    if ([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT) {
      $Acl = Get-Acl $KeyPath
      $Acl.SetAccessRuleProtection($true, $false)
      foreach ($Rule in @($Acl.Access)) { $Acl.RemoveAccessRuleSpecific($Rule) }
      $Identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
      $Acl.SetOwner(([Security.Principal.NTAccount]::new($Identity)))
      $Acl.AddAccessRule(([Security.AccessControl.FileSystemAccessRule]::new($Identity, 'Read', 'Allow')))
      Set-Acl -Path $KeyPath -AclObject $Acl
    } else { & chmod 600 $KeyPath }
    $Endpoint = (DC port mission 2222 | Out-String).Trim()
    if ($Endpoint -notmatch '^127\.0\.0\.1:(\d+)$') { throw 'SSH debe estar publicado solo en 127.0.0.1. Ejecuta up.' }
    $SshPort = $Matches[1]
    $HostPublicKey = (DC exec -T workstation cat /journal/host_ed25519.pub | Out-String).Trim()
    Write-Utf8 'artifacts/ssh/known_hosts' @("[127.0.0.1]:$SshPort $HostPublicKey")
    & ssh -i $KeyPath -p $SshPort -o IdentitiesOnly=yes -o ForwardAgent=no -o StrictHostKeyChecking=yes -o UserKnownHostsFile=artifacts/ssh/known_hosts student@127.0.0.1
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo abrir SSH. Revisa docs/SSH.md.' }
  }
  down { DC --profile ai --profile tools --profile scanners down }
  status { DC --profile ai ps }
  discover { if ($Zone -notin @('public','support')) { throw 'Zona: public o support' }; DC run --rm --no-deps "probe-$Zone" discover }
  probe { if ($Zone -notin @('public','support')) { throw 'Zona: public o support' }; DC run --rm --no-deps "probe-$Zone" probe $Action }
  sbom {
    docker image save vulncorp-records:0.1.0 -o artifacts/images/records.tar; if ($LASTEXITCODE -ne 0) { throw 'Ejecuta up primero.' }
    docker image save vulncorp-core:0.1.0 -o artifacts/images/mission.tar; if ($LASTEXITCODE -ne 0) { throw 'No se pudo exportar mission.' }
    $Lines = @(DC run --rm --no-deps syft docker-archive:/input/records.tar -o cyclonedx-json)
    Write-Utf8 'artifacts/sbom-records.cdx.json' $Lines
    $Lines = @(DC run --rm --no-deps syft docker-archive:/input/mission.tar -o cyclonedx-json)
    Write-Utf8 'artifacts/sbom-mission.cdx.json' $Lines
    Write-Utf8 'artifacts/syft-version.txt' @(DC run --rm --no-deps syft version)
    Write-Host 'SBOMs reales guardados en artifacts/.'
  }
  scan {
    if (-not (Test-Path artifacts/sbom-records.cdx.json)) { throw 'Ejecuta sbom primero.' }
    $Lines = @(DC run --rm --no-deps grype sbom:/reports/sbom-records.cdx.json -o json)
    Write-Utf8 'artifacts/grype-records.json' $Lines
    Write-Utf8 'artifacts/grype-db-status.txt' @(DC run --rm --no-deps grype db status)
    Write-Host 'Reporte completo en artifacts/grype-records.json; el juego ejecuta su propio escaneo en aplicaciones.'
  }
  ai-prepare {
    DC -f compose.yaml -f compose.preload.yaml --profile ai up -d --wait ollama
    $Model = if ($env:OLLAMA_MODEL) { $env:OLLAMA_MODEL } else { 'qwen3:1.7b' }
    try { DC exec -T ollama ollama pull $Model }
    finally { DC --profile ai up -d --wait --force-recreate ollama }
    Write-Host 'Pesos descargados y egreso temporal retirado. Sigue con ai-on.'
  }
  ai-on { DC --profile ai up -d --wait mission ollama; Write-Host 'IA CPU activa; puestos y servicios siguen activos.' }
  ai-off { DC --profile ai stop ollama; Write-Host 'IA detenida; puestos, servicios y medidas permanecen activos.' }
  test { DC run --rm --no-deps check }
  smoke { DC exec -T mission python -m tests.smoke }
  export { $Lines = @(DC exec -T mission python -c 'import json; from app.server import export_bundle; print(json.dumps(export_bundle(),ensure_ascii=False,indent=2))'); Write-Utf8 'artifacts/expediente.json' $Lines; Write-Host 'Expediente guardado.' }
  reset-targets { DC restart gateway records backup; Write-Host 'Targets reiniciados; bitacora conservada.' }
  default { throw 'Comando no reconocido. Ejecuta .\lab.ps1 help' }
}
