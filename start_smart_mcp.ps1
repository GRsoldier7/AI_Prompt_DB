# Smart MCP Server Manager PowerShell Script
Write-Host "=================================================="
Write-Host "SMART MCP SERVER MANAGER" -ForegroundColor Green
Write-Host "=================================================="
Write-Host "This script will:"
Write-Host "1. Scan all ports to find available ones"
Write-Host "2. Start all MCP servers on available ports"
Write-Host "3. Provide a clean shutdown mechanism"
Write-Host "=================================================="
Write-Host ""

# Check if Node.js is installed
try {
    $nodeVersion = node -v
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking required packages..."
try {
    npm list dotenv --depth=0 | Out-Null
    Write-Host "dotenv package is installed" -ForegroundColor Green
} catch {
    Write-Host "Installing dotenv package..." -ForegroundColor Yellow
    npm install dotenv
}

# Function to find all open ports
function Get-OpenPorts {
    Write-Host "Scanning for open ports..." -ForegroundColor Yellow
    $openPorts = @()
    $usedPorts = @()
    
    # Get all TCP connections
    $connections = netstat -ano | Select-String "LISTENING"
    
    foreach ($conn in $connections) {
        $parts = $conn -split '\s+'
        if ($parts.Count -ge 2) {
            $addressPart = $parts[2]
            if ($addressPart -match ':(\d+)$') {
                $port = [int]$matches[1]
                $usedPorts += $port
            }
        }
    }
    
    Write-Host "Found $($usedPorts.Count) ports in use" -ForegroundColor Yellow
    return $usedPorts
}

# Display open ports
$usedPorts = Get-OpenPorts
Write-Host "Used ports: $($usedPorts -join ', ')" -ForegroundColor Cyan

# Run the smart MCP server manager
Write-Host ""
Write-Host "Starting Smart MCP Server Manager..." -ForegroundColor Green
Write-Host ""

# Start the Node.js script
node smart_mcp_server.js

# If the script exits, wait for user input
Write-Host ""
Write-Host "All MCP servers have been stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
