# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# --- THE IMPORTANT CHANGE IS HERE ---
# Copy the lightweight requirements file and rename it inside the container
COPY requirements-free.txt ./requirements.txt

# Install only the needed packages specified in requirements-free.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt')"

# Copy the rest of the application code
COPY ./app /app/app
COPY ./main.py /app/main.py

# Command to run the app when the container launches
CMD ["uvicorn", "app.webhook_handler:app", "--host", "0.0.0.0", "--port", "8000"]