# Use a Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY app/ .

# Expose the port the Flask app will run on (default is 5000)
EXPOSE 5000

# Define environment variables (optional)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Run the Flask app when the container starts
CMD ["python", "app.py"]
