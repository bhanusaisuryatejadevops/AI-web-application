
# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt from app folder
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ .

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]

