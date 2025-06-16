# Use Python 3.10 slim base
FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libgl1-mesa-glx git && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Streamlit-specific environment settings
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=10000
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Expose the port
EXPOSE 10000

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
