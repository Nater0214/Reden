FROM python:3.11.3

# Directory stuff
COPY . /app
WORKDIR /app

# Install packages
RUN apt-get update && apt-get install -y \
net-tools \
libgl1-mesa-glx \
libegl1-mesa \
libxkbcommon-x11-0 \
libdbus-1-3 \
libxcb1 \
libxcb-cursor0 \
libxcb-icccm4 \
libxcb-keysyms1 \
libxcb-shape0

# Install python requirements
RUN python -m pip install -r requirements.txt

ENV QT_DEBUG_PLUGINS=1
ENV DISPLAY=

CMD python main.py