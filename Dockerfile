# =============================================================================
# PRODUCTION DOCKERFILE FOR RAG CHATBOT (OPTIMIZED - MULTI-STAGE)
# =============================================================================

# Stage 1: Build stage - Install dependencies with build tools
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for pip
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_USER=1

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to user directory
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage - Final lightweight image
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Create non-root user first
RUN useradd -m -u 1000 appuser

# Copy only installed packages from builder stage to user's local directory
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
