FROM condaforge/mambaforge:latest

WORKDIR /app

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*


# Copy environment file
COPY environment.yml .

# Create conda environment
RUN mamba env create -f environment.yml

# Copy application code 
COPY . .

# Set environment
ENV PATH="/opt/conda/envs/face_recog_env/bin:${PATH}"

EXPOSE 5000
CMD ["python", "app.py"]   



# FROM condaforge/mambaforge:latest

# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
#     libgtk2.0-0 \
#     libsm6 \
#     libxext6 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy environment.yml from backend folder
# COPY environment.yml /app/environment.yml

# # Create environment with Mamba
# RUN mamba env create -f /app/environment.yml

# # Set environment path
# ENV PATH /opt/conda/envs/face_recog_env/bin:$PATH

# # Copy all backend files correctly
# COPY backend /app

# # Ensure correct working directory
# WORKDIR /app

# EXPOSE 5000

# # Run Flask app
# CMD ["python", "backend/app.py"]





 