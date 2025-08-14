@echo off
REM UAV Image Analysis Platform Deployment Script for Windows
REM This script helps you deploy the UAV project quickly on Windows

echo 🚁 UAV Image Analysis Platform Deployment
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "processed" mkdir processed

REM Build and start the application
echo 🔨 Building and starting the application...
docker-compose up --build -d

REM Wait for the application to start
echo ⏳ Waiting for the application to start...
timeout /t 10 /nobreak >nul

REM Check if the application is running
curl -f http://localhost:5000/api >nul 2>&1
if errorlevel 1 (
    echo ❌ Application failed to start. Check logs with: docker-compose logs uav-app
    pause
    exit /b 1
) else (
    echo ✅ Application is running successfully!
    echo.
    echo 🌐 Access your application at: http://localhost:5000
    echo 📊 API documentation at: http://localhost:5000/api
    echo.
    echo 📝 Useful commands:
    echo   - View logs: docker-compose logs -f uav-app
    echo   - Stop application: docker-compose down
    echo   - Restart application: docker-compose restart
    echo   - Update application: docker-compose up --build -d
    echo.
    echo 🎉 Deployment completed successfully!
)

pause 