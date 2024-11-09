FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy pyproject.toml and poetry.lock for dependency installation
COPY ./pyproject.toml ./poetry.lock* /app/

# Install Poetry dependencies
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/app

# Install Chromium, ChromeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    apt-get clean

# Set environment variables for Selenium to locate Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Copy scripts, alembic.ini, and app files
COPY ./scripts/ /app/
COPY ./alembic.ini /app/
COPY ./prestart.sh /app/
COPY ./tests-start.sh /app/
COPY ./app /app/app

# Show installed packages for verification
RUN poetry run pip list
