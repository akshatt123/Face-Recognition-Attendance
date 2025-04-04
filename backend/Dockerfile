# Use Mambaforge base image
FROM condaforge/mambaforge:latest
    
WORKDIR /app

# Set timezone non-interactively
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    libgtk2.0-0 \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy environment file
COPY environment.yml /app/environment.yml

# Create Conda environment
RUN mamba env create -f /app/environment.yml

# Set the default shell to ensure the environment is activated when needed
SHELL ["/bin/bash", "-c"]

# Copy entire project
COPY . /app

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application using face_env
CMD ["bash", "-c", "conda run --no-capture-output -n face_env python app.py"]
