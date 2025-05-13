FROM public.ecr.aws/lambda/python:3.11

# Install only essential build tools (no audio libs)
RUN yum install -y \
    gcc \
    gcc-c++ \
    make \
    libsndfile \
    ffmpeg \
    zlib-devel \
    libjpeg-turbo-devel \
    freetype-devel \
    openssl-devel \
    git \
    wget \
    curl \
    unzip \
    && yum clean all

WORKDIR /var/task

# Copy project files
COPY pyproject.toml .
COPY . .

# Install Python deps (assumes no pyaudio in pyproject.toml)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# AWS Lambda handler
CMD ["app.handler"]

