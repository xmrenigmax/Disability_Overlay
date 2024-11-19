# Use an official OpenJDK runtime as a parent image
FROM openjdk:8-jdk

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

# Set environment variables
ENV ANDROID_SDK_ROOT=/sdk
ENV PATH=${PATH}:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools:${ANDROID_SDK_ROOT}/emulator

# Download and install Android SDK command line tools
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-7302050_latest.zip -O /sdk-tools.zip && \
    mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    unzip /sdk-tools.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    mv ${ANDROID_SDK_ROOT}/cmdline-tools/latest/cmdline-tools/* ${ANDROID_SDK_ROOT}/cmdline-tools/latest/ && \
    rm -rf ${ANDROID_SDK_ROOT}/cmdline-tools/latest/cmdline-tools && \
    rm /sdk-tools.zip

# Accept licenses
RUN yes | ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager --licenses

# Install necessary SDK packages
RUN ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager "platform-tools" "platforms;android-30"

# Install a single system image
RUN ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager "system-images;android-29;google_apis;x86"

# Install Android Emulator
RUN ${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin/sdkmanager "emulator"

# Set the working directory
WORKDIR /workspace

# Default command
CMD ["bash"]