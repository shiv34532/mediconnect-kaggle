# MediConnect Deployment
# Demonstrates: Deployability (Docker containerization)

FROM python:3.11-slim

# Security: Run as non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port for ADK web server
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3   CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run ADK web server
# Demonstrates: Agent skills (adk web CLI)
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
