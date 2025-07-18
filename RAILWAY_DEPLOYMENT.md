# 🚀 Railway Deployment Guide for AI Recruitment Platform

This guide will help you deploy your AI Recruitment Platform to Railway, which supports larger dependencies and is perfect for your use case.

## 🎯 Why Railway?

- ✅ **No Size Limits**: Unlike Vercel's 250MB limit
- ✅ **Full Python Support**: All your dependencies work
- ✅ **PostgreSQL Database**: Built-in database support
- ✅ **Easy Deployment**: Simple Git-based deployment
- ✅ **Affordable**: $5/month credit, very reasonable pricing
- ✅ **Production Ready**: Auto-scaling, SSL, custom domains

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: Ensure you have your API keys ready

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

Your repository should have these files:
```
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/v1/
│   │   ├── api.py             # API router
│   │   └── endpoints/
│   │       ├── resume.py      # Resume parsing
│   │       └── job_description.py
│   └── services/
│       ├── file_processors.py # File processing
│       ├── groq_service.py    # Groq AI integration
│       └── vector_service.py  # Milvus integration
├── requirements.txt           # All dependencies
├── Procfile                  # Railway process file
├── railway.json             # Railway configuration
└── README.md
```

### Step 2: Deploy to Railway

#### Option A: Deploy via Railway Dashboard

1. **Go to [railway.app](https://railway.app) and sign in**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**
5. **Railway will automatically detect it's a Python app**

#### Option B: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Deploy from your project directory**:
   ```bash
   railway up
   ```

### Step 3: Configure Environment Variables

In your Railway dashboard, go to **Variables** and add:

```env
# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
MISTRAL_API_KEY=your_mistral_api_key_here

# Milvus Vector Database
MILVUS_HOST=your_milvus_host_here
MILVUS_PORT=443
MILVUS_USER=your_milvus_user_here
MILVUS_PASSWORD=your_milvus_password_here
MILVUS_DB_NAME=your_milvus_db_name_here
MILVUS_USE_SECURE=true
MILVUS_TOKEN=your_milvus_token_here

# Vector Collections
RESUME_COLLECTION_NAME=resume_embeddings_mistral
JOB_COLLECTION_NAME=job_embeddings_mistral
EMBEDDING_DIMENSION=1024

# Scoring Weights
SKILLS_MATCH_WEIGHT=0.7
EXPERIENCE_MATCH_WEIGHT=0.2
LOCATION_MATCH_WEIGHT=0.1

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500

# Application Settings
DEBUG=false
ALLOWED_ORIGINS=["*"]
MAX_FILE_SIZE=4194304
PROJECT_NAME=AI Recruitment Platform
API_V1_STR=/api/v1
```

### Step 4: Add PostgreSQL Database (Optional)

1. **In Railway dashboard, click "New"**
2. **Select "Database" → "PostgreSQL"**
3. **Railway will automatically add DATABASE_URL to your variables**

### Step 5: Test Your Deployment

Once deployed, test your endpoints:

1. **Health Check**: `https://your-app.railway.app/health`
2. **API Documentation**: `https://your-app.railway.app/api/v1/docs`
3. **Resume Parser**: `POST https://your-app.railway.app/api/v1/resume/parse`

## 📊 Railway Features

### **Auto-Deployment**
- **GitHub Integration**: Automatic deployments on push to main branch
- **Preview Deployments**: Automatic preview deployments for pull requests
- **Rollback**: Easy rollback to previous versions

### **Monitoring & Logs**
- **Real-time Logs**: View logs in Railway dashboard
- **Performance Metrics**: Monitor response times and errors
- **Health Checks**: Automatic health monitoring

### **Scaling**
- **Auto-scaling**: Based on traffic
- **Manual Scaling**: Adjust replicas as needed
- **Resource Limits**: Configurable CPU and memory

## 🔧 Configuration Files

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 💰 Pricing

### **Free Tier**
- $5/month credit
- 512MB RAM per service
- 1GB storage
- Unlimited requests
- Custom domains

### **Paid Plans**
- **Starter**: $5/month (what you get with free credit)
- **Developer**: $20/month (more resources)
- **Team**: $50/month (team features)

## 🛠️ Development Workflow

### **Local Development**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Link to your Railway project
railway link

# Run locally with Railway environment
railway run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Deployment Commands**
```bash
# Deploy to Railway
railway up

# View logs
railway logs

# Open in browser
railway open
```

## 🔍 Troubleshooting

### **Common Issues**

#### Issue: Build Fails
**Solution**: 
- Check `requirements.txt` for syntax errors
- Ensure all dependencies are compatible
- Check Railway logs for specific errors

#### Issue: Environment Variables Not Working
**Solution**:
- Verify variable names in Railway dashboard
- Ensure no extra spaces in values
- Redeploy after adding variables

#### Issue: Database Connection Fails
**Solution**:
- Check DATABASE_URL in Railway variables
- Ensure database is provisioned
- Verify connection string format

## 📈 Performance Optimization

### **For Railway**
1. **Use async/await**: For I/O operations
2. **Optimize imports**: Only import what you need
3. **Use connection pooling**: For database connections
4. **Implement caching**: Reduce API calls

### **For File Processing**
1. **Stream processing**: Don't load entire files into memory
2. **Size limits**: Respect Railway's limits
3. **Format validation**: Validate files before processing
4. **Error handling**: Graceful fallbacks for failures

## 🎯 Success Metrics

Your deployment is successful when:
- ✅ Health check returns `{"status": "healthy"}`
- ✅ API docs are accessible at `/api/v1/docs`
- ✅ Resume parsing works with all file types
- ✅ Vector embeddings are stored in Milvus
- ✅ Response times are under 10 seconds

## 🔗 Useful Links

- [Railway Documentation](https://docs.railway.app/)
- [Railway Dashboard](https://railway.app/dashboard)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Railway CLI](https://docs.railway.app/reference/cli)

## 🚀 Alternative Platforms

If Railway doesn't work for you, here are other options:

### **Render.com**
- Free tier: 750 hours/month
- Easy deployment
- PostgreSQL support
- Good for Python apps

### **DigitalOcean App Platform**
- $200 credit for 60 days
- Reliable and scalable
- Good documentation
- Production-ready

### **Google Cloud Run**
- 2 million requests/month free
- Serverless architecture
- Auto-scaling
- Pay-per-use pricing

---

**🎉 Congratulations!** Your AI Recruitment Platform is now deployed on Railway with full functionality and no size restrictions! 