ARG VARIANT=3.11-slim
FROM python:${VARIANT} as python_base

# Image Properties
LABEL version="0.3"
LABEL description="Image for SMIT application"

# Configure sources
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list

FROM python_base as smith_base

# Install base packages with apt
RUN apt-get update && apt-get install -y \
    python3-tk \
    --no-install-recommends firefox 
RUN apt-get autoremove -y \
    && apt-get clean -y
RUN pip install poetry

# Application Dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

FROM smith_base as smith_runtime

WORKDIR /smit

# Application setup
COPY . /smit/
RUN poetry install

# Default command, Arguments to `docker run` will be appended
ENTRYPOINT ["poetry", "run", "python", "main.py"]