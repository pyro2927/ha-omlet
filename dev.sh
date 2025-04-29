#!/bin/bash

# Development script for Omlet Home Assistant integration

# Function to display help
show_help() {
  echo "Omlet Home Assistant Integration Development Script"
  echo ""
  echo "Usage: ./dev.sh [command]"
  echo ""
  echo "Commands:"
  echo "  start       - Start the Home Assistant container"
  echo "  stop        - Stop the Home Assistant container"
  echo "  restart     - Restart the Home Assistant container"
  echo "  logs        - Show Home Assistant logs"
  echo "  shell       - Open a shell in the Home Assistant container"
  echo "  help        - Show this help message"
  echo ""
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  echo "Error: Docker is not installed. Please install Docker first."
  exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
  echo "Error: Docker Compose is not installed. Please install Docker Compose first."
  exit 1
fi

# Process commands
case "$1" in
  start)
    echo "Starting Home Assistant container..."
    docker-compose up -d
    echo "Home Assistant is running at http://localhost:8123"
    ;;
  stop)
    echo "Stopping Home Assistant container..."
    docker-compose down
    ;;
  restart)
    echo "Restarting Home Assistant container..."
    docker-compose restart
    ;;
  logs)
    echo "Showing Home Assistant logs..."
    docker-compose logs -f
    ;;
  shell)
    echo "Opening shell in Home Assistant container..."
    docker-compose exec homeassistant /bin/bash
    ;;
  help|*)
    show_help
    ;;
esac 