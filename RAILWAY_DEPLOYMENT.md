# Railway Deployment Guide for AI Recruitment Platform

## 🚀 Quick Deploy to Railway

### Option 1: Deploy via Railway Dashboard
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Railway will automatically detect the configuration and deploy

### Option 2: Deploy via Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy from your project directory
railway up
```

## 🔧 Configuration Files

### Railway Configuration (`railway.json`)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python railway_start.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "numReplicas": 1
  }
}
```

### Startup Script (`railway_start.py`)
- Properly handles `$PORT` environment variable
- Includes error handling and logging
- Optimized for Railway's serverless environment

### Procfile
```
web: python railway_start.py
```

## 🌍 Environment Variables

Set these in your Railway project dashboard:

### Required Variables
```env
# AI Services
GROQ_API_KEY=your_groq_api_key
MISTRAL_API_KEY=your_mistral_api_key

# Vector Database (Milvus/Zilliz)
MILVUS_HOST=your_milvus_host
MILVUS_PORT=19530
MILVUS_USER=your_milvus_user
MILVUS_PASSWORD=your_milvus_password
MILVUS_TOKEN=your_milvus_token
MILVUS_USE_SECURE=true

# Application Settings
MAX_FILE_SIZE=4194304
EMBEDDING_DIMENSION=1024
```

### Optional Variables
```env
# Debug and Logging
DEBUG=false
LOG_LEVEL=info

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500

# Vector Collections
RESUME_COLLECTION_NAME=resume_embeddings_mistral
JOB_COLLECTION_NAME=job_embeddings_mistral
```

## 📊 Health Checks

The application includes multiple health check endpoints:

### Main Health Check
```bash
GET /health
```

### Railway-Specific Health Check
```bash
GET /api/v1/health/railway
```

### Service Status
```bash
GET /
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Configuration Error
**Error**: `Invalid value for '--port': '$PORT' is not a valid integer`

**Solution**: The `railway_start.py` script properly handles the PORT environment variable:
```python
port = int(os.environ.get("PORT", 8000))
```

#### 2. Build Failures
**Error**: Build process fails during dependency installation

**Solution**: 
- Check `requirements-railway.txt` for compatible versions
- Ensure all dependencies are available for Python 3.11
- Use the Railway-specific requirements file

#### 3. Service Connection Issues
**Error**: Vector database or AI service connection failures

**Solution**:
- Verify environment variables are set correctly
- Check API keys and credentials
- Ensure services are accessible from Railway's network

#### 4. Memory Issues
**Error**: Application runs out of memory

**Solution**:
- Railway provides 512MB RAM by default
- Optimize dependencies in `requirements-railway.txt`
- Use lightweight processing for large files

### Debug Commands

#### Check Railway Logs
```bash
railway logs
```

#### View Environment Variables
```bash
railway variables
```

#### Restart Service
```bash
railway service restart
```

## �� Deployment Steps

### 1. Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Railway deployment ready"
git push origin main
```

### 2. Deploy to Railway
```bash
# Option A: Use Railway CLI
railway up

# Option B: Use deployment script
./railway_deploy.sh
```

### 3. Configure Environment Variables
1. Go to Railway Dashboard
2. Select your project
3. Go to "Variables" tab
4. Add all required environment variables

### 4. Test Deployment
```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Test API documentation
curl https://your-app.railway.app/docs
```

## 📈 Monitoring

### Railway Dashboard
- **Deployments**: View deployment history and status
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, and network usage
- **Variables**: Environment variable management

### Application Monitoring
- **Health Checks**: Automatic health monitoring
- **Error Logging**: Comprehensive error tracking
- **Performance**: Response time monitoring

## 🔄 Continuous Deployment

### GitHub Integration
1. Connect your GitHub repository to Railway
2. Enable automatic deployments on push
3. Railway will automatically deploy on every commit

### Manual Deployment
```bash
# Deploy specific branch
railway up --branch feature-branch

# Deploy with custom environment
railway up --environment production
```

## 🛡️ Security

### Environment Variables
- Never commit sensitive data to Git
- Use Railway's secure variable storage
- Rotate API keys regularly

### CORS Configuration
```python
# Configured for development
ALLOWED_ORIGINS: List[str] = ["*"]
```

### Rate Limiting
```python
RATE_LIMIT_PER_MINUTE: int = 30
RATE_LIMIT_PER_HOUR: int = 500
```

## 📝 API Endpoints

### Core Endpoints
- `POST /api/v1/resume/parse` - Parse resume files
- `POST /api/v1/jobs/match` - Match candidates for jobs
- `GET /health` - Health check
- `GET /docs` - API documentation

### Railway-Specific Endpoints
- `GET /api/v1/health/railway` - Railway health check
- `GET /` - Root endpoint with status

## 🎯 Best Practices

### 1. Environment Management
- Use different environments for dev/staging/prod
- Never expose sensitive data in logs
- Use Railway's variable encryption

### 2. Performance Optimization
- Keep dependencies minimal
- Use async operations where possible
- Implement proper error handling

### 3. Monitoring
- Set up alerts for critical errors
- Monitor response times
- Track API usage patterns

### 4. Security
- Validate all inputs
- Implement proper authentication
- Use HTTPS for all communications

## 🆘 Support

### Railway Support
- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

### Application Support
- Check logs for detailed error messages
- Use health check endpoints for diagnostics
- Monitor Railway dashboard for system status

## 🚀 Next Steps

1. **Deploy your application** using the steps above
2. **Configure environment variables** in Railway dashboard
3. **Test all endpoints** to ensure functionality
4. **Set up monitoring** and alerts
5. **Integrate with your frontend** application
6. **Monitor performance** and optimize as needed

Your AI Recruitment Platform should now be successfully deployed on Railway! 🎉 