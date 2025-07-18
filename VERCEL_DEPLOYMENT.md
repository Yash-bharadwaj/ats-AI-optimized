# 🚀 Vercel Deployment Guide for AI Recruitment Platform

This guide will help you deploy your AI Recruitment Platform to Vercel with optimizations for size restrictions and performance.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **API Keys**: Ensure you have your API keys ready:
   - Groq API Key
   - Mistral AI API Key
   - Milvus/Zilliz Cloud credentials

## 🔧 Optimizations Made for Vercel

### ✅ **Size Optimizations**
- **Removed Heavy Dependencies**:
  - `Pillow` (PIL) - replaced with lightweight alternatives
  - `pytesseract` - OCR not needed for Vercel
  - `pymupdf` - replaced with `PyPDF2`
  - `psycopg2-binary` - PostgreSQL removed for Vercel

- **Lightweight File Processing**:
  - Uses `PyPDF2` instead of `PyMuPDF`
  - Supports only PDF, DOCX, and TXT files
  - Removed image processing capabilities

- **Reduced Bundle Size**:
  - Only essential endpoints included
  - Removed complex job/applicant management endpoints
  - Focused on core resume and job parsing

### ✅ **Performance Optimizations**
- **Async Processing**: All file operations are async
- **Memory Efficient**: Stream processing for large files
- **Timeout Handling**: 30-second function timeout
- **Error Recovery**: Graceful fallbacks for AI failures

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure your code is in a GitHub repository**
2. **Verify the optimized files are present**:
   ```
   ├── app/
   │   ├── main_vercel.py          # Vercel-optimized main
   │   ├── api/v1/
   │   │   ├── api_vercel.py       # Vercel-optimized router
   │   │   └── endpoints/
   │   │       ├── resume_vercel.py # Vercel-optimized resume parser
   │   │       └── job_description.py
   │   └── services/
   │       └── file_processors_vercel.py # Lightweight file processor
   ├── requirements-vercel.txt      # Optimized dependencies
   ├── vercel.json                 # Vercel configuration
   └── VERCEL_DEPLOYMENT.md        # This guide
   ```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com) and sign in**
2. **Click "New Project"**
3. **Import your GitHub repository**
4. **Configure the project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements-vercel.txt`

#### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**:
   ```bash
   vercel
   ```

### Step 3: Configure Environment Variables

In your Vercel dashboard, go to **Settings > Environment Variables** and add:

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

### Step 4: Test Your Deployment

Once deployed, test your endpoints:

1. **Health Check**: `https://your-app.vercel.app/health`
2. **API Documentation**: `https://your-app.vercel.app/api/v1/docs`
3. **Resume Parser**: `POST https://your-app.vercel.app/api/v1/resume/parse`

## 📊 Monitoring and Debugging

### Vercel Dashboard Features
- **Function Logs**: View real-time logs in Vercel dashboard
- **Performance Metrics**: Monitor response times and errors
- **Environment Variables**: Manage secrets securely

### Common Issues and Solutions

#### Issue: Function Timeout (30s)
**Solution**: 
- Optimize file processing
- Reduce file size limits
- Use async processing

#### Issue: Bundle Size Too Large
**Solution**:
- Remove unused dependencies
- Use lightweight alternatives
- Split into multiple functions

#### Issue: Environment Variables Not Working
**Solution**:
- Check variable names in Vercel dashboard
- Ensure no extra spaces in values
- Redeploy after adding variables

## 🔄 Continuous Deployment

### Automatic Deployments
- **GitHub Integration**: Automatic deployments on push to main branch
- **Preview Deployments**: Automatic preview deployments for pull requests
- **Environment Management**: Separate environments for staging/production

### Manual Deployments
```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel
```

## 📈 Performance Optimization Tips

### For Vercel Functions
1. **Keep functions small**: Focus on single responsibility
2. **Use async/await**: For I/O operations
3. **Optimize imports**: Only import what you need
4. **Cache responses**: Use Vercel's edge caching

### For File Processing
1. **Stream processing**: Don't load entire files into memory
2. **Size limits**: Respect Vercel's 4MB limit
3. **Format validation**: Validate files before processing
4. **Error handling**: Graceful fallbacks for failures

## 🛠️ Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements-vercel.txt

# Run locally
uvicorn app.main_vercel:app --host 0.0.0.0 --port 8000
```

### Testing Before Deployment
```bash
# Test locally
curl -X POST http://localhost:8000/api/v1/resume/parse \
  -F "file=@test_resume.pdf" \
  -F "candidate_id=test123"
```

## 📞 Support

If you encounter issues:

1. **Check Vercel Logs**: Dashboard > Functions > View Logs
2. **Test Locally**: Ensure it works locally first
3. **Review Environment Variables**: Verify all are set correctly
4. **Check Bundle Size**: Ensure dependencies are optimized

## 🎯 Success Metrics

Your deployment is successful when:
- ✅ Health check returns `{"status": "healthy"}`
- ✅ API docs are accessible at `/api/v1/docs`
- ✅ Resume parsing works with PDF/DOCX files
- ✅ Vector embeddings are stored in Milvus
- ✅ Response times are under 10 seconds

## 🔗 Useful Links

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)

---

**🎉 Congratulations!** Your AI Recruitment Platform is now deployed on Vercel with optimized performance and minimal bundle size. 