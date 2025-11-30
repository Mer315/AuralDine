@echo off
REM AuralDine Docker Commands
REM This script provides easy access to common Docker operations

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================
echo    AuralDine Docker Command Menu
echo ========================================
echo.
echo 1. Build and Start (docker-compose up --build)
echo 2. Start services (use existing images)
echo 3. Stop services (containers remain)
echo 4. Remove services (containers deleted)
echo 5. View all logs
echo 6. View backend logs
echo 7. View frontend logs
echo 8. Check container status
echo 9. Clean up everything (images + containers)
echo 10. Exit
echo.
set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" goto build_start
if "%choice%"=="2" goto start_only
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto down
if "%choice%"=="5" goto logs_all
if "%choice%"=="6" goto logs_backend
if "%choice%"=="7" goto logs_frontend
if "%choice%"=="8" goto status
if "%choice%"=="9" goto cleanup
if "%choice%"=="10" goto end
echo Invalid choice. Please try again.
timeout /t 2 /nobreak
goto menu

:build_start
echo.
echo Building and starting all services...
echo.
docker-compose up --build
goto menu

:start_only
echo.
echo Starting services with existing images...
echo.
docker-compose up
goto menu

:stop
echo.
echo Stopping services...
echo.
docker-compose stop
echo Services stopped. Containers remain.
timeout /t 2 /nobreak
goto menu

:down
echo.
echo Removing services...
echo.
docker-compose down
echo Services removed.
timeout /t 2 /nobreak
goto menu

:logs_all
echo.
echo Showing all logs (Ctrl+C to stop)...
echo.
docker-compose logs -f
goto menu

:logs_backend
echo.
echo Showing backend logs (Ctrl+C to stop)...
echo.
docker-compose logs -f backend
goto menu

:logs_frontend
echo.
echo Showing frontend logs (Ctrl+C to stop)...
echo.
docker-compose logs -f frontend
goto menu

:status
echo.
echo Container status:
echo.
docker-compose ps
echo.
echo Service health:
echo.
docker ps --format "table {{.Names}}\t{{.Status}}"
echo.
pause
goto menu

:cleanup
echo.
echo WARNING: This will remove all images and containers!
echo.
set /p confirm="Are you sure? (yes/no): "
if /i "%confirm%"=="yes" (
    echo Stopping services...
    docker-compose down -v
    echo Pruning Docker system...
    docker system prune -a --volumes -f
    echo Cleanup complete.
) else (
    echo Cleanup cancelled.
)
timeout /t 2 /nobreak
goto menu

:end
echo.
echo Exiting...
endlocal
exit /b
