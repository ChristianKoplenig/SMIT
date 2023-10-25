ARG VARIANT=3-bookworm
FROM python:${VARIANT}

# Image Properties
LABEL version="0.2"
LABEL description="Image for SMIT application"

# Install Firefox
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

# Jupyter Kernel
RUN python3 -m pip install ipykernel