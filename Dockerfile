########### STAGE 1 ###########
FROM python:3.9.15 AS base
ARG USERNAME=thereisnospoon
ARG POETRY_VERSION=1.2.0
# Setup the user
RUN useradd -ms /bin/bash "${USERNAME}"
USER "${USERNAME}"

# Copy all files
WORKDIR "$HOME/app"
COPY . "$HOME/app"

# Install poetry
# RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -
RUN POETRY_VERSION=$POETRY_VERSION python3 install-poetry.py

# Install dependancies and build
RUN $HOME/.local/bin/poetry install
RUN $HOME/.local/bin/poetry build


########### STAGE 2 ###########
FROM python:3.9.15-slim AS final
ARG USERNAME=thereisnospoon

# Setup user
RUN useradd -ms /bin/bash "${USERNAME}"
USER "${USERNAME}"

# Copy files
WORKDIR "$HOME/app"
COPY --from=base $HOME/app/dist/*.whl $HOME/app/dist/
# Install package
RUN pip install dist/*.whl
