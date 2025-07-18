# Railway Deployment Guide for AI Recruitment Platform

## 🚀 Railway-Optimized Deployment

This guide will help you deploy the AI Recruitment Platform on Railway with all advanced features intact.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be on GitHub
3. **Environment Variables**: Prepare your API keys and configuration

## 🔧 Environment Variables Setup

Set these environment variables in your Railway project:

### API Keys
```
GROQ_API_KEY=your_groq_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Milvus Vector Database
```
MILVUS_HOST=your_milvus_host
MILVUS_PORT=443
MILVUS_USER=your_milvus_user
MILVUS_PASSWORD=your_milvus_password
MILVUS_DB_NAME=your_database_name
MILVUS_USE_SECURE=true
MILVUS_TOKEN=your_milvus_token
```

### Collection Names
```
RESUME_COLLECTION_NAME=resume_embeddings_mistral
JOB_COLLECTION_NAME=job_embeddings_mistral
EMBEDDING_DIMENSION=1024
```

### Matching Weights
```
SKILLS_MATCH_WEIGHT=0.7
EXPERIENCE_MATCH_WEIGHT=0.2
LOCATION_MATCH_WEIGHT=0.1
```

### Rate Limiting
```
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500
```

### Application Settings
```
DEBUG=false
ALLOWED_ORIGINS=["*"]
MAX_FILE_SIZE=4194304
PROJECT_NAME="AI Recruitment Platform"
API_V1_STR=/api/v1
```

## 🚀 Deployment Steps

### Step 1: Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your repository: `Yash-bharadwaj/ats-AI-optimized`
6. Select the `fresh-start` branch

### Step 2: Configure Environment Variables

1. In your Railway project dashboard, go to "Variables"
2. Add all the environment variables listed above
3. Make sure to use your actual API keys and database credentials

### Step 3: Deploy

1. Railway will automatically detect the Dockerfile
2. The build process will use the Railway-optimized requirements
3. Deployment should complete successfully without buildkit errors

### Step 4: Verify Deployment

1. Check the deployment logs for any errors
2. Visit your Railway domain (e.g., `https://your-app.railway.app`)
3. Test the health endpoint: `https://your-app.railway.app/health`
4. Test the API docs: `https://your-app.railway.app/docs`

## 🔍 Testing Your Deployment

### Health Check
```bash
curl https://your-app.railway.app/health
```

### Resume Parsing
```bash
curl -X POST https://your-app.railway.app/api/v1/resume/parse \
  -F "file=@resume.pdf" \
  -F "candidate_id=test_candidate"
```

### Job Matching
```bash
curl -X POST https://your-app.railway.app/api/v1/jobs/match \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "skills": ["python", "react", "aws"],
    "experience_years": 3,
    "location": "Remote"
  }'
```

## 🛠️ Railway-Optimized Features

### ✅ What's Included

1. **Lightweight File Processing**
   - PDF processing with PyPDF2
   - DOCX processing with python-docx
   - TXT file support
   - No heavy image processing dependencies

2. **Railway-Optimized Resume Parser**
   - Basic text extraction
   - Regex-based information extraction
   - AI analysis with Groq API
   - Skills and experience analysis
   - Graceful fallbacks for missing dependencies

3. **Vector Database Integration**
   - Milvus Cloud integration
   - Embedding generation with Mistral AI
   - Resume storage and retrieval
   - Candidate matching

4. **API Endpoints**
   - `/api/v1/resume/parse` - Parse resumes
   - `/api/v1/jobs/match` - Match candidates to jobs
   - `/api/v1/health/railway` - Railway health check
   - `/health` - Basic health check
   - `/docs` - API documentation

### 🚫 What's Excluded (for Railway compatibility)

1. **Heavy Dependencies**
   - Pillow (PIL) - causes buildkit errors
   - scikit-learn - too large for Railway
   - Complex image processing
   - Heavy ML libraries

2. **Advanced Features**
   - OCR processing
   - Image enhancement
   - Complex file format support
   - Advanced ML models

## 🔧 Troubleshooting

### Build Failures

**Problem**: Docker buildkit errors
**Solution**: The Railway-optimized version removes all heavy dependencies that cause buildkit issues.

**Problem**: Import errors
**Solution**: All imports are wrapped in try-catch blocks with graceful fallbacks.

### Runtime Errors

**Problem**: Missing modules
**Solution**: The app provides fallback functionality when modules are unavailable.

**Problem**: API key errors
**Solution**: Check that all environment variables are set correctly in Railway.

### Performance Issues

**Problem**: Slow response times
**Solution**: The Railway version is optimized for speed with minimal dependencies.

## 📊 Monitoring

### Railway Dashboard
- Monitor deployment status
- Check logs for errors
- View resource usage

### Health Endpoints
- `/health` - Basic health check
- `/api/v1/health/railway` - Detailed service health

### API Documentation
- `/docs` - Interactive API documentation
- `/redoc` - Alternative API documentation

## 🔄 Updates and Maintenance

### Updating the Application
1. Make changes to your code
2. Commit and push to GitHub
3. Railway will automatically redeploy

### Environment Variable Updates
1. Go to Railway dashboard
2. Update variables in the "Variables" section
3. Redeploy the application

### Scaling
1. Railway automatically scales based on traffic
2. Monitor usage in the Railway dashboard
3. Upgrade plan if needed

## 🎯 Success Criteria

Your deployment is successful when:

1. ✅ Build completes without errors
2. ✅ Health check returns `200 OK`
3. ✅ API documentation is accessible
4. ✅ Resume parsing works
5. ✅ Job matching works
6. ✅ Vector database integration works

## 📞 Support

If you encounter issues:

1. Check the Railway deployment logs
2. Verify all environment variables are set
3. Test locally with the Railway requirements
4. Check the health endpoints for service status

## 🚀 Next Steps

After successful deployment:

1. Test all API endpoints
2. Upload sample resumes
3. Test job matching functionality
4. Monitor performance
5. Set up monitoring and alerts

---

**🎉 Congratulations!** Your AI Recruitment Platform is now deployed on Railway with all core features working! 