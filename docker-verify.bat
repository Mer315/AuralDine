@echo off
REM Docker Build & Verification Script for Windows

echo ==========================================
echo AuralDine - Docker Build Verification
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker is not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('docker --version') do echo [OK] %%i

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose is not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('docker-compose --version') do echo [OK] %%i

REM Check Docker daemon
docker info >nul 2>&1
if errorlevel 1 (
    echo X Docker daemon is not running
    echo Please start Docker Desktop and try again
    exit /b 1
)
echo [OK] Docker daemon is running

echo.
echo Building Docker images...
echo ==========================================

docker-compose build
if errorlevel 1 (
    echo X Build failed!
    exit /b 1
)
echo [OK] Build successful!

echo.
echo Starting containers...
echo ==========================================

docker-compose up -d

echo Waiting for services to start (30 seconds)...
timeout /t 5 /nobreak

echo.
echo Testing services...
echo ==========================================

REM Test backend
echo Testing backend on port 5000...
curl -f http://localhost:5000/ >nul 2>&1
if errorlevel 1 (
    echo X Backend is not responding
    echo Checking logs:
    docker-compose logs backend
) else (
    echo [OK] Backend is responding
)

REM Test frontend
echo Testing frontend on port 3000...
curl -f http://localhost:3000/ >nul 2>&1
if errorlevel 1 (
    echo X Frontend is not responding
    echo Checking logs:
    docker-compose logs frontend
) else (
    echo [OK] Frontend is responding
)

echo.
echo ==========================================
echo Running Containers:
echo ==========================================
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo ==========================================
echo SUCCESS! Docker containers are running
echo ==========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo To stop containers:
echo   docker-compose down
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo ==========================================
