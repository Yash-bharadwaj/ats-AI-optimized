#!/bin/bash

# 🚀 Vercel Deployment Script for AI Recruitment Platform
# This script helps prepare and deploy your app to Vercel

echo "🚀 Starting Vercel deployment preparation..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Please run this script from the project root."
    exit 1
fi

# Check if optimized files exist
echo "📋 Checking optimized files..."
files_to_check=(
    "app/main_vercel.py"
    "app/api/v1/api_vercel.py"
    "app/api/v1/endpoints/resume_vercel.py"
    "app/services/file_processors_vercel.py"
    "requirements-vercel.txt"
    "vercel.json"
)

for file in "${files_to_check[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done

echo "✅ All optimized files are present!"

# Check if user is logged into Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
fi

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your Vercel dashboard"
echo "2. Add environment variables (see VERCEL_DEPLOYMENT.md)"
echo "3. Test your endpoints"
echo "4. Monitor performance in Vercel dashboard"
echo ""
echo "🔗 Useful links:"
echo "- Vercel Dashboard: https://vercel.com/dashboard"
echo "- Deployment Guide: VERCEL_DEPLOYMENT.md" 