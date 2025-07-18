# Railway Deployment Guide for AI Recruitment Platform

## Overview
This guide provides step-by-step instructions for deploying the AI Recruitment Platform on Railway with optimized settings for production use.

## Prerequisites
- Railway account
- GitHub repository with the project
- API keys for Groq and Mistral AI
- Milvus Cloud account

## Environment Variables Setup

### Required Environment Variables
Set these in your Railway project dashboard:

```bash
# API Keys
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key

# Milvus Cloud Configuration
MILVUS_HOST=your_milvus_host
MILVUS_PORT=443
MILVUS_USER=your_milvus_user
MILVUS_PASSWORD=your_milvus_password
MILVUS_DB_NAME=your_database_name
MILVUS_USE_SECURE=true
MILVUS_TOKEN=your_milvus_token

# Collection Names
RESUME_COLLECTION_NAME=resume_embeddings_mistral
JOB_COLLECTION_NAME=job_embeddings_mistral

# Platform Configuration
EMBEDDING_DIMENSION=1024
SKILLS_MATCH_WEIGHT=0.7
EXPERIENCE_MATCH_WEIGHT=0.2
LOCATION_MATCH_WEIGHT=0.1

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500

# Security and CORS
DEBUG=false
ALLOWED_ORIGINS=["*"]
MAX_FILE_SIZE=4194304

# Project Information
PROJECT_NAME="AI Recruitment Platform"
API_V1_STR=/api/v1
```

## Deployment Steps

### 1. Connect Repository
1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the main branch

### 2. Configure Build Settings
Railway will automatically detect the Python project. The build process uses:
- `requirements-railway.txt` for dependencies
- `Procfile` for startup command
- Python 3.11 runtime

### 3. Set Environment Variables
1. Go to your project in Railway dashboard
2. Navigate to "Variables" tab
3. Add all required environment variables listed above
4. Save changes

### 4. Deploy
1. Railway will automatically start the deployment
2. Monitor the build logs for any issues
3. Wait for deployment to complete

## Railway-Optimized Features

### Lightweight File Processing
- Uses `Pillow` for basic image processing
- `PyPDF2` for PDF text extraction
- `python-docx` for Word document processing
- No heavy dependencies like `pytesseract` or `opencv-python`

### Optimized AI Analysis
- Shorter prompts for faster processing
- Reduced token limits for cost efficiency
- Graceful fallbacks for API failures

### Advanced Matching
- Full-featured matching algorithms
- Vector-based similarity search
- Comprehensive scoring system

## API Endpoints

### Railway-Optimized Endpoints
- `POST /api/v1/railway/parse-railway` - Parse resumes with Railway optimization
- `POST /api/v1/railway/match-candidates-railway` - Find matching candidates
- `POST /api/v1/railway/calculate-match-score-railway` - Calculate match scores
- `GET /api/v1/railway/candidate/{id}/profile-railway` - Get candidate profiles
- `GET /api/v1/railway/health/railway` - Railway health check

### Standard Endpoints (Still Available)
- `POST /api/v1/resume/parse` - Standard resume parsing
- `POST /api/v1/advanced/parse-advanced` - Advanced parsing (if dependencies available)

## Troubleshooting

### Build Failures
If the build fails due to dependencies:

1. **Check requirements-railway.txt**: Ensure all dependencies are compatible
2. **Verify Python version**: Railway uses Python 3.11
3. **Check build logs**: Look for specific error messages

### Runtime Errors
Common issues and solutions:

1. **Import Errors**:
   ```bash
   # Check if all modules are properly imported
   # Railway-optimized services should handle missing dependencies gracefully
   ```

2. **Memory Issues**:
   - Railway provides 8GB RAM by default
   - Optimized services use less memory
   - Monitor memory usage in Railway dashboard

3. **API Timeouts**:
   - Reduced timeout settings for Railway
   - Graceful error handling for API failures

### Environment Variable Issues
1. **Missing Variables**: Ensure all required variables are set
2. **Invalid Values**: Check API keys and connection strings
3. **CORS Issues**: Verify `ALLOWED_ORIGINS` setting

## Performance Optimization

### Railway-Specific Optimizations
1. **Lightweight Dependencies**: Uses minimal dependencies
2. **Efficient Processing**: Optimized file processing algorithms
3. **Smart Caching**: Vector database for fast searches
4. **Graceful Degradation**: Services work even with missing dependencies

### Monitoring
1. **Railway Dashboard**: Monitor logs and performance
2. **Health Checks**: Use `/health` endpoint
3. **API Metrics**: Track response times and errors

## Testing the Deployment

### Health Check
```bash
curl https://your-railway-app.railway.app/health
```

### Parse Resume
```bash
curl -X POST "https://your-railway-app.railway.app/api/v1/railway/parse-railway" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

### Railway Health Check
```bash
curl https://your-railway-app.railway.app/api/v1/railway/health/railway
```

## Production Considerations

### Security
1. **API Keys**: Keep API keys secure
2. **CORS**: Configure allowed origins properly
3. **Rate Limiting**: Monitor API usage

### Scalability
1. **Railway Auto-scaling**: Automatic scaling based on traffic
2. **Database**: Milvus Cloud handles vector storage
3. **Caching**: Vector embeddings for fast searches

### Cost Optimization
1. **API Usage**: Monitor Groq and Mistral API usage
2. **Railway Credits**: Monitor Railway resource usage
3. **Efficient Processing**: Lightweight algorithms reduce costs

## Support

### Railway Support
- Railway documentation: https://docs.railway.app/
- Railway Discord: https://railway.app/discord

### Platform Issues
- Check logs in Railway dashboard
- Use health check endpoints
- Monitor API response times

## Migration from Vercel

If migrating from Vercel:

1. **Export Environment Variables**: Copy all variables to Railway
2. **Update Dependencies**: Use `requirements-railway.txt`
3. **Test Endpoints**: Verify all functionality works
4. **Update Documentation**: Point to new Railway URLs

## Conclusion

The Railway deployment provides:
- ✅ Reliable deployment with 8GB RAM
- ✅ Full advanced features with lightweight optimization
- ✅ Automatic scaling and monitoring
- ✅ Cost-effective production deployment
- ✅ Comprehensive error handling and logging

Your AI Recruitment Platform is now ready for production use on Railway! 