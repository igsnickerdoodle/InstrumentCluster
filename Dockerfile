FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libx11-xcb1 \
    libxrender1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libxrender1 \
    libqt5core5a \
    libqt5gui5 \
    libqt5widgets5 \
    unclutter \
    qt5-qmake \
    python3-pyqt5 \
    pyqt5-dev-tools \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m abc
RUN usermod -a -G 44,105 abc
# Set the working directory in the container
WORKDIR /usr/src/app

# Switch to the non-root user
USER abc

# Copy the application source code from your host to the container
COPY --chown=abc:abc InstrumentCluster/ .

# Install Python dependencies as the non-root user
RUN pip3 install --user --no-cache-dir -r requirements.txt
RUN pip3 install --user PyQt5

# Create a startup script to disable screen blanking and run the application
RUN echo "#!/bin/bash\n\
xset s off\n\
xset -dpms\n\
xset s noblank\n\
unclutter -idle 0.1 -root\n\
exec python3 /usr/src/app/main.py" > /usr/src/app/start.sh && chmod +x /usr/src/app/start.sh

RUN mkdir -p /tmp/runtime-root && \
    chown abc:abc /tmp/runtime-root && \
    chmod 0700 /tmp/runtime-root

# Command to run on container start
CMD ["/usr/src/app/start.sh"]
