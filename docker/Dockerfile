FROM python:3.12-slim AS base

# Install curl (required for uv installer) and clean up apt lists
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Ensure uv is on PATH
ENV PATH="/root/.local/bin:${PATH}"
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY docker/.streamlit /app/.streamlit
# Install Python dependencies
COPY docker/requirements.txt .
RUN uv venv /opt/venv
RUN uv pip install -r requirements.txt

FROM base AS development

RUN apt-get update && apt-get install -y openssh-server unzip wget && rm -rf /var/lib/apt/lists/*

COPY docker/id_ed25519_development /etc/ssh/ssh_host_ed25519_key
COPY docker/id_ed25519_development.pub /etc/ssh/ssh_host_ed25519_key.pub
COPY docker/authorized_keys /root/.ssh/authorized_keys

RUN mkdir -p /root/.vscodium-server/extensions && \
# Download Python extension
wget -O /tmp/ms-python.python-2025.16.0.vsix \
    "https://open-vsx.org/api/ms-python/python/2025.16.0/file/ms-python.python-2025.16.0.vsix" && \
# Download Debugpy extension (Linux x64)
wget -O /tmp/ms-python.debugpy-2025.14.1.vsix \
    "https://open-vsx.org/api/ms-python/debugpy/linux-x64/2025.14.1/file/ms-python.debugpy-2025.14.1@linux-x64.vsix" && \
# Install Python extension
unzip /tmp/ms-python.python-2025.16.0.vsix -d /tmp/py && \
mv /tmp/py/extension /root/.vscodium-server/extensions/ms-python.python-2025.16.0 && \
# Install Debugpy extension
unzip /tmp/ms-python.debugpy-2025.14.1.vsix -d /tmp/debugpy && \
mv /tmp/debugpy/extension /root/.vscodium-server/extensions/ms-python.debugpy-2025.14.1 && \
# Clean up
rm -rf /tmp/py /tmp/debugpy /tmp/*.vsix

FROM base AS production

WORKDIR /app
COPY src src
COPY app.py app.py
COPY .env .env

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
