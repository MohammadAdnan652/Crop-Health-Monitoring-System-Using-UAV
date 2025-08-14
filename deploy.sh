#!/bin/bash

# UAV Image Analysis Platform Deployment Script
# This script helps you deploy the UAV project quickly

set -e

echo "🚁 UAV Image Analysis Platform Deployment"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads processed

# Build and start the application
echo "🔨 Building and starting the application..."
docker-compose up --build -d

# Wait for the application to start
echo "⏳ Waiting for the application to start..."
sleep 10

# Check if the application is running
if curl -f http://localhost:5000/api > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🌐 Access your application at: http://localhost:5000"
    echo "📊 API documentation at: http://localhost:5000/api"
    echo ""
    echo "📝 Useful commands:"
    echo "  - View logs: docker-compose logs -f uav-app"
    echo "  - Stop application: docker-compose down"
    echo "  - Restart application: docker-compose restart"
    echo "  - Update application: docker-compose up --build -d"
    echo ""
    echo "🎉 Deployment completed successfully!"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs uav-app"
    exit 1
fi 