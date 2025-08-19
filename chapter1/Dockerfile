# Use an official Python runtime as a parent image

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for some Python packages (e.g., for building wheels)
# This step is often necessary for packages like `uvicorn` or `gunicorn`
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --reload flag enables auto-reloading during development (remove for production)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
