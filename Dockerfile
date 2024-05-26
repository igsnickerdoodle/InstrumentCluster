FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    arduino \
    arduino-core \
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
    qt5-qmake \
    python3-pyqt5 \
    pyqt5-dev-tools \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m abc && \
    usermod -a -G 44,105 abc && \
    usermod -a -G dialout abc

WORKDIR /usr/src/app

USER abc

COPY --chown=abc:abc /var/app/InstrumentCluster/ .

RUN pip3 install --user --no-cache-dir -r requirements.txt
RUN pip3 install --user PyQt5

RUN echo "#!/bin/bash\n\
xset s off\n\
xset -dpms\n\
xset s noblank\n\
exec python3 /usr/src/app/main.py" > /usr/src/app/start.sh && chmod +x /usr/src/app/start.sh

RUN mkdir -p /tmp/runtime-root && \
    chown abc:abc /tmp/runtime-root && \
    chmod 0700 /tmp/runtime-root

CMD ["/usr/src/app/start.sh"]
