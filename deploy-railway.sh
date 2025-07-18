#!/bin/bash

# 🚀 Railway Deployment Script for AI Recruitment Platform
# This script helps prepare and deploy your app to Railway

echo "🚀 Starting Railway deployment preparation..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if we're in the right directory
if [ ! -f "railway.json" ]; then
    echo "❌ railway.json not found. Please run this script from the project root."
    exit 1
fi

# Check if required files exist
echo "📋 Checking required files..."
files_to_check=(
    "app/main.py"
    "app/api/v1/api.py"
    "app/api/v1/endpoints/resume.py"
    "app/services/file_processors.py"
    "requirements.txt"
    "railway.json"
    "Procfile"
)

for file in "${files_to_check[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done

echo "✅ All required files are present!"

# Check if user is logged into Railway
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "🔐 Please log in to Railway..."
    railway login
fi

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Add environment variables (see RAILWAY_DEPLOYMENT.md)"
echo "3. Test your endpoints"
echo "4. Monitor performance in Railway dashboard"
echo ""
echo "🔗 Useful links:"
echo "- Railway Dashboard: https://railway.app/dashboard"
echo "- Deployment Guide: RAILWAY_DEPLOYMENT.md" 