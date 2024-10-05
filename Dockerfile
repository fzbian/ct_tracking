FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create virtual environment (optional but recommended)
RUN python3 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt

# Expose ports for UI and API
EXPOSE 8000 8001

# Run the application
CMD ["sh", "-c", "source venv/bin/activate && python ui/manage.py runserver 0.0.0.0:8000 & uvicorn main:app --reload --port 8001 & wait $!"]