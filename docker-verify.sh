#!/bin/bash
# Docker Build & Verification Script

echo "=========================================="
echo "AuralDine - Docker Build Verification"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed"
    exit 1
fi
echo "✓ Docker installed: $(docker --version)"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose is not installed"
    exit 1
fi
echo "✓ Docker Compose installed: $(docker-compose --version)"

# Check if Docker daemon is running
if ! docker info > /dev/null 2>&1; then
    echo "✗ Docker daemon is not running"
    exit 1
fi
echo "✓ Docker daemon is running"

echo ""
echo "Building Docker images..."
echo "=========================================="

# Build images
docker-compose build

if [ $? -eq 0 ]; then
    echo "✓ Build successful!"
else
    echo "✗ Build failed!"
    exit 1
fi

echo ""
echo "Testing containers..."
echo "=========================================="

# Start in background
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check backend
echo "Testing backend..."
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    echo "✓ Backend is responding"
else
    echo "✗ Backend is not responding"
    docker-compose logs backend
fi

# Check frontend
echo "Testing frontend..."
if curl -f http://localhost:3000/ > /dev/null 2>&1; then
    echo "✓ Frontend is responding"
else
    echo "✗ Frontend is not responding"
    docker-compose logs frontend
fi

echo ""
echo "=========================================="
echo "Summary:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "=========================================="
echo "To stop containers: docker-compose down"
echo "To view logs: docker-compose logs -f"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:5000"
