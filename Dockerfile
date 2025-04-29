# Use an official lightweight Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install fastapi uvicorn streamlit

# Expose ports
# 8501 = Streamlit UI
# 8000 = FastAPI API
EXPOSE 8501
EXPOSE 8000

# Set environment variables (optional)
ENV OPENAI_API_KEY=your-key-here
ENV GCG_API_KEY=your-api-key-here

# Command to run API by default (can override)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

