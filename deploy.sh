#!/bin/bash

# Production Deployment Script for Google Sheets API Service

set -e

echo "🚀 Starting production deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build the new image
echo "🔨 Building Docker image..."
docker-compose build --no-cache

# Start the service
echo "▶️ Starting the service..."
docker-compose up -d

# Wait for the service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 10

# Check if the service is running
echo "🔍 Checking service health..."
if curl -f http://localhost:5000/matches > /dev/null 2>&1; then
    echo "✅ Service is running successfully!"
    echo "🌐 API is available at: http://localhost:5000/matches"
    echo "📊 Health check endpoint: http://localhost:5000/matches"
else
    echo "❌ Service failed to start properly."
    echo "📋 Checking logs..."
    docker-compose logs
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop service: docker-compose down"
echo "  Restart service: docker-compose restart"
echo "  Check status: docker-compose ps"
