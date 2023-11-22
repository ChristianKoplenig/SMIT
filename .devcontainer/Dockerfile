ARG VARIANT=3.11-slim
FROM python:${VARIANT}

# Image Properties
LABEL version="0.2"
LABEL description="Image for SMIT application"

# Configure sources
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list

# Install additional packages
RUN apt-get update && apt-get install -y \
    python3-tk \
    --no-install-recommends firefox 

RUN apt-get autoremove -y \
    && apt-get clean -y

# Project Folder
WORKDIR /smit

# Pip requirements
COPY ../config/requirements_docker.txt /smit/requirements.txt
RUN pip3 install -r requirements.txt

# Application setup
COPY . /smit/
RUN pip3 install -e .

# Default command, Arguments to `docker run` will be appended
ENTRYPOINT ["python", "main.py"]