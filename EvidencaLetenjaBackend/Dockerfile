FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory (including the 'app' folder and everything else)
COPY . .

ENV PYTHONPATH=/app/app
# Set the PYTHONPATH environment variable to the correct working directory
# This will allow Python to locate the modules, including 'core'

# Expose the port on which the FastAPI application will run
EXPOSE 8000

#
# Run the FastAPI application using uvicorn, pointing to the main module inside the 'app' folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
