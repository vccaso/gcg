# Use slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (override via docker run -e)
ENV OPENAI_API_KEY=changeme

# Default command
CMD ["python", "run_cli.py", "--workflow", "workflows/wf_angular.yaml"]
