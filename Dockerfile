
# First a base image has to be selected. I am using the official Python 3.12 image based on leightweight Alpine
FROM python:3.12-alpine

# RUN allows to execute arbitrary shell commands, creating a new file system layer
# Best Practice: create a dedicated user to run you application otherwise it is run a root
# RUN busybox addgroup -S -g 6969 tempstore && busybox adduser -h /app -G tempstore -D -u 6969 tempstore

ARG POETRY_VERSION=1.7.1


ENV POETRY_VIRTUALENVS_IN_PROJECT=True

# The following installs Poetry in the given version
# one may use something called `here-documents` to write multiple lines of shell commands
# for this a few external dependencies have to be installed (GCC etc)
RUN <<EOF sh
    apk add --no-cache \
            curl \
            gcc \
            libressl-dev \
            musl-dev \
            libffi-dev
    python3 -m pip install --upgrade pip
    python3 -m pip install --no-cache-dir poetry==${POETRY_VERSION}
EOF

# change working directory to /app, would create it if not exists
WORKDIR /app


# Copy pyproject.toml and install dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy the rest of the application code
COPY ./src ./src
COPY tests .


RUN poetry install

# ENV to run
ENV PORT = 8000

# Expose the port the app runs on
EXPOSE 8000


# command to execute on container startup
# first create the generic entry command (poetry in this case, which would allow us to run Python as well)
ENTRYPOINT ["poetry", "run"]
# CMD then runs poetry with the default flags
CMD ["./src/main.py", "uvicorn", "--host", "0.0.0.0", "--port", "8000"]
