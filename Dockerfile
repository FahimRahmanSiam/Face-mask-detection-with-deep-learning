FROM python:3.10-slim

WORKDIR /app

# --- Install system packages needed for OpenCV, PyAV, and aiortc ---
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    pkg-config \
    libavdevice-dev \
    libavfilter-dev \
    libopus-dev \
    libvpx-dev \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libswscale-dev \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- Install Python dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install cython  # PyAV needs this to build
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy your app code ---
COPY . .

EXPOSE 10000

CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
