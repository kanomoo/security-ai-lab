<#
.SYNOPSIS
    Quick Ask script for Windows PowerShell
.EXAMPLE
    .\ask.ps1 -Prompt "เขียนสคริปต์สแกนพอร์ต" -Url "https://your-tunnel.trycloudflare.com"
#>
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Prompt,

    [Parameter(Mandatory=$false)]
    [string]$Url = $env:LLM_API_URL,

    [Parameter(Mandatory=$false)]
    [string]$Model = "huihui_ai/qwen2.5-coder-abliterated:14b"
)

if (-not $Url) {
    $Url = "http://localhost:11434"
}

$Url = $Url.TrimEnd('/')
$endpoint = "$Url/api/generate"

$body = @{
    model = $Model
    prompt = $Prompt
    stream = $false
} | ConvertTo-Json

Write-Host "[-] Connecting to $Model via $Url..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri $endpoint -Method Post -Body $body -ContentType "application/json" -TimeoutSec 120
    Write-Host "`n[Response]:" -ForegroundColor Green
    Write-Host $response.response
}
catch {
    Write-Host "[!] Error connecting to API: $_" -ForegroundColor Red
}
