FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libx11-6 \
    libgl1-mesa-glx \
    libpulse0 \
    libnss3 \
    libxi6 \
    libxkbfile1 \
    libxrender1 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    mesa-utils \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxext6 \
    libxau6 \
    libxdmcp6 \
    libxinerama1 \
    libxrandr2 \
    libxss1 \
    libxt6 \
    libsm6 \
    libice6 \
    xvfb

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run main_app.py when the container launches
CMD ["python", "main_app.py"]