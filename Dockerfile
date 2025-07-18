FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements-railway.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-railway.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run the application using the start script
CMD ["./start.sh"] 