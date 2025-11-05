# Grant Management System Setup Script
# Run this script to set up the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Grant Management System Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Check if MySQL is installed
Write-Host "`nChecking MySQL installation..." -ForegroundColor Yellow
try {
    mysql --version | Out-Null
    Write-Host "✓ MySQL found" -ForegroundColor Green
} catch {
    Write-Host "✗ MySQL is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install MySQL from https://dev.mysql.com/downloads/" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Configuration
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Database Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default MySQL Configuration:" -ForegroundColor Yellow
Write-Host "  Host: localhost"
Write-Host "  User: root"
Write-Host "  Password: (empty)"
Write-Host "  Database: grant_management"
Write-Host ""

$configureDb = Read-Host "Do you want to change database settings? (y/N)"

if ($configureDb -eq "y" -or $configureDb -eq "Y") {
    Write-Host "`nNote: You can also edit config.py manually later" -ForegroundColor Gray
    Write-Host ""
    
    $dbHost = Read-Host "MySQL Host (default: localhost)"
    if ([string]::IsNullOrWhiteSpace($dbHost)) { $dbHost = "localhost" }
    
    $user = Read-Host "MySQL User (default: root)"
    if ([string]::IsNullOrWhiteSpace($user)) { $user = "root" }
    
    $password = Read-Host "MySQL Password (press Enter if none)"
    
    # Update config.py
    $configContent = @"
# Database Configuration
# Modify these settings according to your MySQL setup

DB_CONFIG = {
    'host': '$dbHost',
    'user': '$user',
    'password': '$password',
    'database': 'grant_management'
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    'page_title': 'Grant Management System',
    'page_icon': '',
    'layout': 'wide'
}
"@
    
    Set-Content -Path "config.py" -Value $configContent
    Write-Host "✓ Configuration saved" -ForegroundColor Green
} else {
    Write-Host "Using default configuration" -ForegroundColor Gray
}

# Setup complete
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Make sure MySQL server is running" -ForegroundColor White
Write-Host "2. Run the application with: streamlit run app.py" -ForegroundColor White
Write-Host "3. Open the web browser at: http://localhost:8501" -ForegroundColor White
Write-Host "4. Click 'Initialize Schema' in the sidebar to create tables" -ForegroundColor White
Write-Host ""

$runNow = Read-Host "Do you want to run the application now? (Y/n)"
if ($runNow -ne "n" -and $runNow -ne "N") {
    Write-Host "`nStarting Streamlit application..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""
    streamlit run app.py
}
