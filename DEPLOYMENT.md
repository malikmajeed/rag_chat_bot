# Docker Deployment Guide

## Prerequisites
- Docker installed and running
- Environment variables ready (OPENAI_API_KEY, MONGODB_URI)

## Build the Docker Image

```bash
# Build the image
docker build -t rag-chatbot:latest .

# Or with a specific tag
docker build -t rag-chatbot:v1.0 .
```

## Run the Container

### Option 1: Using Your Existing .env File (Recommended)
If you already have a `.env` file in your project root, you can use it directly:

```bash
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/vector_db:/app/vector_db \
  --restart unless-stopped \
  rag-chatbot:latest
```

**Note**: Your `.env` file should contain:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
MONGODB_URI=mongodb://localhost:27017
```

### Option 2: Pass Environment Variables Directly
```bash
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  -e MONGODB_URI=mongodb://localhost:27017 \
  -v $(pwd)/vector_db:/app/vector_db \
  --restart unless-stopped \
  rag-chatbot:latest
```

### Option 3: Production Run (with External MongoDB)
```bash
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  --env-file .env \
  -e MONGODB_URI=mongodb://your_mongodb_host:27017 \
  -v $(pwd)/vector_db:/app/vector_db \
  --restart unless-stopped \
  rag-chatbot:latest
```

### Option 4: Create Separate Docker Environment File
If you want to keep your local `.env` separate from Docker:

```bash
# Create .env.docker file (don't commit this to git!)
cat > .env.docker << EOF
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb://your_mongodb_host:27017
EOF

# Run with env file
docker run -d \
  --name rag-chatbot \
  -p 8000:8000 \
  --env-file .env.docker \
  -v $(pwd)/vector_db:/app/vector_db \
  --restart unless-stopped \
  rag-chatbot:latest
```

**Security Note**: Make sure `.env.docker` is in your `.gitignore` if you create it!

## Useful Docker Commands

### View Logs
```bash
# View logs
docker logs rag-chatbot

# Follow logs in real-time
docker logs -f rag-chatbot

# View last 100 lines
docker logs --tail 100 rag-chatbot
```

### Container Management
```bash
# Stop container
docker stop rag-chatbot

# Start container
docker start rag-chatbot

# Restart container
docker restart rag-chatbot

# Remove container
docker rm rag-chatbot

# Remove container and volumes
docker rm -v rag-chatbot
```

### Execute Commands in Container
```bash
# Access container shell
docker exec -it rag-chatbot /bin/bash

# Run Python command
docker exec rag-chatbot python -c "print('Hello')"

# Check health
docker exec rag-chatbot python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read())"
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi rag-chatbot:latest

# Remove all unused images
docker image prune -a
```

### Container Status
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container stats
docker stats rag-chatbot

# Inspect container
docker inspect rag-chatbot
```

## Health Check

The container includes a health check. View health status:

```bash
docker ps  # Check STATUS column for (healthy) or (unhealthy)
```

Or test manually:
```bash
curl http://localhost:8000/health
```

## Access the Application

- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs rag-chatbot

# Check if port is already in use
lsof -i :8000
```

### Permission issues with volumes
```bash
# Fix permissions (if needed)
sudo chown -R 1000:1000 ./vector_db
```

### Rebuild after code changes
```bash
# Stop and remove old container
docker stop rag-chatbot && docker rm rag-chatbot

# Rebuild image
docker build -t rag-chatbot:latest .

# Run again
docker run -d --name rag-chatbot -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e MONGODB_URI=your_uri \
  -v $(pwd)/vector_db:/app/vector_db \
  rag-chatbot:latest
```

## Docker Compose (Alternative)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  rag-chatbot:
    build: .
    container_name: rag-chatbot
    ports:
      - "8000:8000"
    env_file:
      - .env  # Loads variables from your .env file
    volumes:
      - ./vector_db:/app/vector_db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Then run:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

**Note**: Docker Compose will automatically load variables from your `.env` file using `env_file`.

