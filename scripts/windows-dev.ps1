<#!
PowerShell helper script for Windows users to replicate common Makefile targets:
- make dev
- make install-n8n

Usage examples (from repository root):
    pwsh -File .\scripts\windows-dev.ps1 dev
    pwsh -File .\scripts\windows-dev.ps1 install-n8n

You can also dot-source and call functions:
    . .\scripts\windows-dev.ps1
    Invoke-Dev
    Install-N8N

Requirements:
- Docker Desktop for Windows must be installed and running.
- PowerShell 7+ (recommended).
- Port availability similar to UNIX setup.
#>

param(
    [Parameter(Position=0)]
    [ValidateSet('dev','install-n8n','help')]
    [string]$Command = 'help'
)

$ErrorActionPreference = 'Stop'

$ComposeFile = 'docker-compose.yaml'
$Blue = "`e[36m"; $Green = "`e[32m"; $Yellow = "`e[33m"; $Red = "`e[31m"; $Nc = "`e[0m"

function Write-Info($msg) { Write-Host "${Blue}$msg${Nc}" }
function Write-Success($msg) { Write-Host "${Green}$msg${Nc}" }
function Write-Warn($msg) { Write-Host "${Yellow}$msg${Nc}" }
function Write-Err($msg) { Write-Host "${Red}$msg${Nc}" }

function Assert-Docker() {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Err 'Docker CLI not found. Please install Docker Desktop and ensure docker is on PATH.'
        exit 1
    }
}

function Invoke-Dev() {
    Assert-Docker
    Write-Info 'Starting development environment (equivalent to make dev)...'
    docker compose -f $ComposeFile up --build -d
    Write-Success 'Services started successfully!'
    Write-Host 'Frontend:  http://localhost:3001'
    Write-Host 'Backend:   http://localhost:8000'
    Write-Host 'API Docs:  http://localhost:8000/docs'
    Write-Host 'Health:    http://localhost:8000/healthz'
    Write-Host 'Grafana:   http://localhost:3000 (admin/admin)'
    Write-Host 'Elastic:   http://localhost:9200 (elastic/password)'
    Write-Host 'Prometheus:http://localhost:9090'
    Write-Host 'Kibana:    http://localhost:5601 (elastic/password)'
    Write-Info 'Resetting Kibana system password...'
    try {
        curl.exe -X POST "http://localhost:9200/_security/user/kibana_system/_password" -u elastic:password -H "Content-Type: application/json" -d '{"password":"password"}' | Out-Null
        Write-Success 'Kibana system password ensured.'
    }
    catch {
        Write-Warn "Failed to reset kibana_system password: $($_.Exception.Message)"
    }
}

function Install-N8N() {
    Assert-Docker
    Write-Info 'Creating n8n database (equivalent to make install-n8n)...'
    try {
        docker compose -f $ComposeFile exec -T db psql -U postgres -c "CREATE DATABASE n8n;" | Out-Null
        Write-Info 'Restarting n8n service...'
        docker compose -f $ComposeFile restart n8n | Out-Null
        Write-Success 'n8n database created and service restarted.'
    }
    catch {
        Write-Err "Failed to install n8n: $($_.Exception.Message)"
        exit 1
    }
}

function Show-Help() {
    Write-Host 'Windows helper script for MyTodoApp'
    Write-Host 'Commands:'
    Write-Host '  dev          Start development environment'
    Write-Host '  install-n8n  Create n8n DB and restart service'
    Write-Host '  help         Show this help'
    Write-Host ''
    Write-Host 'Examples:'
    Write-Host '  pwsh -File scripts/windows-dev.ps1 dev'
    Write-Host '  pwsh -File scripts/windows-dev.ps1 install-n8n'
}

switch ($Command) {
    'dev' { Invoke-Dev }
    'install-n8n' { Install-N8N }
    'help' { Show-Help }
}
