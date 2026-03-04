# test_simple.ps1 - Simple Flight Catalog API Test
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing Flight Catalog API" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:5001"

# Test 1: Health Check
Write-Host "`n1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing -TimeoutSec 5
    $health = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($health.status)" -ForegroundColor Green
    Write-Host "   Service: $($health.service)"
} catch {
    Write-Host "   Error: Could not connect to server" -ForegroundColor Red
    Write-Host "   Make sure your Flask app is running!"
    exit
}

# Test 2: Get all flights
Write-Host "`n2. Getting All Flights..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/flights/" -UseBasicParsing -TimeoutSec 5
    $flights = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($flights.status)" -ForegroundColor Green
    Write-Host "   Message: $($flights.message)"
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Search flights
Write-Host "`n3. Searching Flights (JFK -> LAX)..." -ForegroundColor Yellow
try {
    # escape ampersand or use single quotes around query string
    $url = "$baseUrl/api/flights/search?departure=JFK`&arrival=LAX"
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    $search = $response.Content | ConvertFrom-Json
    Write-Host "   Status: $($search.status)" -ForegroundColor Green
    Write-Host "   Filters: Departure=$($search.filters.departure), Arrival=$($search.filters.arrival)"
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Tests Completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Ask if user wants to open in browser
$choice = Read-Host "`nOpen API in browser? (y/n)"
if ($choice -eq 'y') {
    Start-Process "http://localhost:5001/api/flights/"
}