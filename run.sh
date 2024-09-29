#!/bin/bash

# Function to display an error message and exit
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <UI_PORT> <API_PORT>"
    exit 1
fi

# Assign input parameters to variables
UI_PORT=$1
API_PORT=$2

# Check if the ports are valid numbers
if ! [[ "$UI_PORT" =~ ^[0-9]+$ ]]; then
    error_exit "UI port must be a valid number."
fi

if ! [[ "$API_PORT" =~ ^[0-9]+$ ]]; then
    error_exit "API port must be a valid number."
fi

# Set up Python virtual environment directory
VENV_DIR="venv"

# Check if the virtual environment exists, if not, create it
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR || error_exit "Failed to create virtual environment."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate || error_exit "Failed to activate virtual environment."

# Check if requirements.txt exists and install the required packages
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt || error_exit "Failed to install dependencies."
else
    error_exit "requirements.txt not found."
fi

# Compile translations
echo "Compiling Django translations..."
django-admin compilemessages || error_exit "Failed to compile translations."

# Run Django server in the background
echo "Starting Django (UI) server on port $UI_PORT..."
python3 ui/manage.py runserver 0.0.0.0:$UI_PORT &

# Capture Django process ID to monitor it
DJANGO_PID=$!

# Run FastAPI server in the background
echo "Starting FastAPI (API) server on port $API_PORT..."
uvicorn main:app --reload --port $API_PORT &

# Capture FastAPI process ID to monitor it
FASTAPI_PID=$!

# Function to clean up and stop both servers
function stop_servers {
    echo "Stopping servers..."
    kill $DJANGO_PID $FASTAPI_PID
    deactivate
    exit 0
}

# Trap signals to stop servers when script is interrupted
trap stop_servers SIGINT SIGTERM

# Wait for both servers to finish or stop manually
echo "Servers are running. Press Ctrl+C to stop."
wait $DJANGO_PID $FASTAPI_PID

# Return exit code if any server stops unexpectedly
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    error_exit "One of the servers stopped unexpectedly. Exit code: $EXIT_CODE"
fi

# Deactivate the virtual environment when done
deactivate
