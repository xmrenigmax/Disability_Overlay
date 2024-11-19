#!/bin/bash

# Start Xvfb
Xvfb :1 -screen 0 1024x768x16 &

# Set the DISPLAY environment variable
export DISPLAY=:1

# Create the AVD if it doesn't exist
if ! avdmanager list avd | grep -q "Name: my_avd"; then
    avdmanager create avd -n my_avd -k "system-images;android-29;google_apis;x86" -d "pixel"
fi

# Run the emulator in headless mode
emulator -avd my_avd -no-window -no-accel -no-audio -no-snapshot -no-metrics