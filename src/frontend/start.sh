#!/bin/bash

# EDGE-QI Frontend Quick Start Script
# Run this script to start the development server

echo "🚀 Starting EDGE-QI Frontend..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Start dev server
echo "✨ Launching development server..."
echo "📍 URL: http://localhost:5173"
echo "🛑 Press Ctrl+C to stop"
echo ""

npm run dev
