# Use an official Python 3.11 image as the base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl wget gnupg software-properties-common apt-transport-https lsb-release sudo && \
    # Install gettext
    apt-get install -y gettext && \
    # Install Node.js and npm
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    # Install PCRE grep
    apt-get install -y pcregrep && \
    apt-get install netcat-openbsd && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /code/

RUN useradd -ms /bin/bash newuser && echo "newuser:password" | chpasswd && adduser newuser sudo
RUN chown -R newuser:newuser /code




RUN chmod +x /code/tools/install.sh
RUN chmod +x /code/tools/migrate.sh
RUN chmod +x /code/tools/load_init_data.sh
RUN chmod +x /code/tools/run.sh



USER newuser

RUN /code/tools/install.sh --python python3.11
RUN /code/tools/migrate.sh --python python3.11
RUN /code/tools/load_init_data.sh --python python3.11