# VULNETT SECURITY SYSTEMS - WINDOWS DEPLOYMENT SCRIPT
$ErrorActionPreference = "Stop"
Write-Host "🚀 Starting Vulnett Environment Initialization..." -ForegroundColor Cyan

# 0. Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ CRITICAL ERROR: Python is not installed. Please install it from https://python.org" -ForegroundColor Red
    exit
}

# 1. Check/Install Nmap
Write-Host "[+] Checking for Nmap..." -ForegroundColor Cyan
$nmapPath = Get-Command nmap -ErrorAction SilentlyContinue
if (!$nmapPath) {
    # Check common installation path
    $commonPath = "C:\Program Files (x86)\Nmap\nmap.exe"
    if (Test-Path $commonPath) {
        Write-Host "[*] Nmap found at $commonPath. Adding to PATH for this session." -ForegroundColor Green
        $env:Path += ";C:\Program Files (x86)\Nmap"
    }
    else {
        Write-Host "[!] Nmap not found. Attempting automatic installation..." -ForegroundColor Yellow
        
        # Try Winget first (modern Windows)
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            Write-Host "[+] Using winget to install Nmap..." -ForegroundColor Cyan
            winget install --id Insecure.Nmap --accept-package-agreements --accept-source-agreements --silent
        }
        else {
            # Manual download and silent install
            Write-Host "[+] Downloading Nmap Installer..." -ForegroundColor Cyan
            $nmapUrl = "https://nmap.org/dist/nmap-7.98-setup.exe"
            $nmapOutput = "$env:TEMP\nmap_setup.exe"
            Invoke-WebRequest -Uri $nmapUrl -OutFile $nmapOutput
            Write-Host "[+] Running Nmap setup silently (this may take a minute)..." -ForegroundColor Cyan
            Start-Process -FilePath $nmapOutput -ArgumentList "/S" -Wait
            
            # Check path again
            if (Test-Path $commonPath) {
                $env:Path += ";C:\Program Files (x86)\Nmap"
                Write-Host "[*] Nmap installed successfully." -ForegroundColor Green
            }
            else {
                Write-Host "⚠️ Warning: Nmap installation finished but path check failed. You may need to restart the terminal." -ForegroundColor Red
            }
        }
    }
}
else {
    Write-Host "[*] Nmap is already available in PATH." -ForegroundColor Green
}

# 2. Install Nuclei
$binPath = "$env:USERPROFILE\bin"
if (!(Test-Path $binPath)) { New-Item -ItemType Directory -Path $binPath | Out-Null }

if (!(Get-Command nuclei -ErrorAction SilentlyContinue)) {
    Write-Host "[+] Downloading Nuclei v3.7.0..." -ForegroundColor Cyan
    $url = "https://github.com/projectdiscovery/nuclei/releases/download/v3.7.0/nuclei_3.7.0_windows_amd64.zip"
    $output = "$env:TEMP\nuclei.zip"
    Invoke-WebRequest -Uri $url -OutFile $output
    Expand-Archive -Path $output -DestinationPath $binPath -Force
    
    # Add to current session path
    $env:Path += ";$binPath"
    Write-Host "[*] Nuclei installed to $binPath and added to current session." -ForegroundColor Green
}
else {
    Write-Host "[*] Nuclei is already installed." -ForegroundColor Green
}

# 3. Setup Python Virtual Environment
$venvPython = ".\.venv\Scripts\python.exe"
if (!(Test-Path $venvPython)) {
    if (Test-Path ".\.venv\bin\python.exe") { $venvPython = ".\.venv\bin\python.exe" }
}

# If venv folder exists but no python.exe, it's corrupted - remove and start over
if ((Test-Path ".venv") -and (!(Test-Path $venvPython))) {
    Write-Host "[!] Existing .venv appears corrupted (python.exe missing). Re-initializing..." -ForegroundColor Yellow
    Remove-Item -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue
}

if (!(Test-Path ".venv")) {
    Write-Host "[+] Creating Python Virtual Environment..." -ForegroundColor Cyan
    # Try 'python' then 'py'
    $pythonCmd = "python"
    if (!(python --version 2>$null)) {
        if (py -3 --version 2>$null) { $pythonCmd = "py -3" }
    }
    
    Invoke-Expression "$pythonCmd -m venv .venv --copies"
    
    # Re-verify path after creation
    $venvPython = ".\.venv\Scripts\python.exe"
    if (!(Test-Path $venvPython)) {
        if (Test-Path ".\.venv\bin\python.exe") { $venvPython = ".\.venv\bin\python.exe" }
        else {
            Write-Host "❌ CRITICAL ERROR: Failed to create virtual environment properly." -ForegroundColor Red
            exit
        }
    }
}

# 4. Install Dependencies
Write-Host "[+] Installing Python Packages..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "`n✅ DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "--------------------------------------"
Write-Host "To start the gateway:"
Write-Host "1. Activate: .\.venv\Scripts\Activate.ps1"
Write-Host "2. Run: python scanner.py"
Write-Host "--------------------------------------"

