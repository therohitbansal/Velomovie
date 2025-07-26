FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg lsb-release \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 libxss1 libxcomposite1 libxdamage1 \
    libgtk-3-0 libxrandr2 xdg-utils ca-certificates fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./chrome.deb && rm chrome.deb

# Set Chrome binary path for undetected-chromedriver
ENV GOOGLE_CHROME_BIN="/usr/bin/google-chrome"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app
WORKDIR /app

# Expose port (if needed)
EXPOSE 8000

# Start app (change if not FastAPI)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
