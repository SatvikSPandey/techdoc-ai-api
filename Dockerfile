# Start from the official Python 3.11 image
# This gives us a clean Linux environment with Python already installed
FROM python:3.11-slim

# Set the working directory inside the container
# All commands after this run from this folder
WORKDIR /app

# Copy requirements first (before copying code)
# Docker caches each step — if requirements haven't changed,
# it skips reinstalling packages on the next build. Faster builds.
COPY requirements.txt .

# Install all packages
RUN pip install --no-cache-dir -r requirements_backend.txt

# Now copy the rest of the code
COPY . .

# Tell Docker this container listens on port 8000
EXPOSE 8000

# The command that runs when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]