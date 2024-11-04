# Set console title
$host.UI.RawUI.WindowTitle = "Video Player App"

# Function to check if Python is installed
function Test-Python {
    try {
        python --version
        return $true
    }
    catch {
        return $false
    }
}

# Function to check if a package is installed
function Test-PythonPackage {
    param($PackageName)
    
    $result = python -c "import $PackageName" 2>&1
    return $LASTEXITCODE -eq 0
}

# Check if Python is installed
if (-not (Test-Python)) {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Create required directories
$dirs = @(
    "static\content",
    "static\subtitles"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Yellow
    }
}

# Check and install required packages
if (-not (Test-PythonPackage "flask")) {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install flask
}

# Start the app
Write-Host "`nStarting Video Player App..." -ForegroundColor Green
Write-Host "Server will be available at http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

try {
    python app.py
}
catch {
    Write-Host "`nError running the app: $_" -ForegroundColor Red
}
finally {
    Read-Host "`nPress Enter to exit"
} 