
# Configuración de log
$logFile = Join-Path $PSScriptRoot "run_log.txt"

function Write-Log {
    param([string]$message, [string]$color = "White")
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $entry = "$timestamp - $message"
    Add-Content -Path $logFile -Value $entry
    Write-Host $message -ForegroundColor $color
}

Write-Log "=== Iniciando aplicación Water Analytics ===" "Cyan"
Set-Location -Path $PSScriptRoot

# Comprobar si existe el script de activación
$venvActivate = ".\.venv\Scripts\Activate.ps1"
if (-Not (Test-Path $venvActivate)) {
    Write-Log "[ERROR] No se encontró el entorno virtual (.venv)." "Red"
    Write-Log "Crea el entorno con: python -m venv .venv" "Yellow"
    Pause
    exit 1
}

# Activar el entorno virtual en la sesión actual
Write-Log "Activando entorno virtual..." "Yellow"
. $venvActivate

# Instalar dependencias si existe requirements.txt
# if (Test-Path ".\requirements.txt") {
#     Write-Log "Instalando dependencias (modo silencioso)..." "Yellow"
#     python -m pip install --upgrade pip --quiet --disable-pip-version-check
#     python -m pip install -r requirements.txt --quiet --disable-pip-version-check
# } else {
#     Write-Log "[AVISO] No se encontró requirements.txt, se omite instalación." "DarkYellow"
# }

# Ejecutar la aplicación
Write-Log "Ejecutando main.py..." "Green"
try {
    python .\src\main.py 2>&1 | Tee-Object -FilePath $logFile -Append
    Write-Log "Ejecución completada." "Green"
} catch {
    Write-Log "[ERROR] Falló la ejecución: $($_.Exception.Message)" "Red"
}

Write-Log "Presiona cualquier tecla para salir..." "Cyan"
Pause
