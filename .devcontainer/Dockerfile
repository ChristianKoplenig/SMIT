ARG VARIANT=3.11-bookworm
FROM python:${VARIANT} as python_base

# Image Properties
LABEL version="0.4"
LABEL description="Image for SMIT application"

# Version Tags
ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.7.1

# Application Arguments
ARG APP_NAME=smit
ARG APP_PATH=/${APP_NAME}
#ARG STL_ENTRY=${APP_PATH}/src/webgui/st_main.py

# Environment setup
ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 
ENV \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:$PATH"


FROM python_base as smit_base
# Install Smit dependencies
WORKDIR $APP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --without dev --no-root

FROM smit_base as smit_runtime
# Install Smit application
COPY . ./
RUN poetry install --without dev

# Run streamlit framework
ENTRYPOINT [ "poetry", "run" ]
CMD [ "streamlit", "run", "src/webgui/st_main.py" ]