FROM python:3.11 

# Set environment variables to prevent Python from writing .pyc files and to ensure output is sent straight away
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file into the container
COPY requirements.txt .

# "docker builder prune -f" Caution: Run this in terminal to clear the cache if you want to force re-installing dependencies

# Install Python dependencies
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy the application code into the container
COPY ./app ./app
# COPY .env .

# Expose the port that the FastAPI app will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
# CMD ["python", "app/main.py"]

#CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4"]
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port \$PORT --workers 4"
