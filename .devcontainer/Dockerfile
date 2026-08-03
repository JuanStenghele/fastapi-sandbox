# Python development image
FROM mcr.microsoft.com/devcontainers/python:3.13

# Install all Python requirements
COPY requirements.txt /tmp/setup/requirements.txt
COPY test/requirements.txt /tmp/setup/test-requirements.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/setup/requirements.txt -r /tmp/setup/test-requirements.txt && rm -rf /tmp/setup
