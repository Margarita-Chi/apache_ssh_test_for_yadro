FROM debian:bookworm-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install Python, utilities, and Java (headless)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     python3 python3-venv python3-pip \
     wget unzip curl ca-certificates \
     default-jre-headless \
  && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt /app/

# Prepare Allure directories with permissions
RUN mkdir -p /app/allure-results /app/allure-report \
    && chown -R 1000:1000 /app/allure-results /app/allure-report \
    && chmod -R 777 /app/allure-results /app/allure-report

# Create virtual environment and install Python packages
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/python -m pip install --upgrade pip setuptools wheel \
  && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy test scripts
COPY tests/ /app/tests/

# Install Allure CLI
ARG ALLURE_VERSION=2.30.0
RUN wget -O /tmp/allure.zip "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip" \
  && unzip /tmp/allure.zip -d /opt/ \
  && mv /opt/allure-${ALLURE_VERSION} /opt/allure \
  && ln -s /opt/allure/bin/allure /usr/bin/allure \
  && rm -f /tmp/allure.zip

# Expose Allure server port
EXPOSE 8080
ENV PATH="/opt/venv/bin:${PATH}"

# Run tests and generate Allure report
CMD ["/bin/bash", "-c", "\
pytest tests/ --alluredir=allure-results -v --cache-clear && \
allure generate allure-results -o allure-report --clean && \
allure open allure-report --port 8080"]

