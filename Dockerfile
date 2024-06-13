FROM python:3.11

WORKDIR /code

RUN apt-get update && \
    apt-get install -y sudo curl wget gnupg software-properties-common apt-transport-https lsb-release sudo postgresql postgresql-contrib && \
    apt-get install -y gettext && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get install -y pcregrep && \
    apt-get install netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /code/
RUN mkdir -p /code/integreat_cms/media/global

RUN chmod +x /code/tools/install.sh
RUN chmod +x /code/tools/migrate.sh
RUN chmod +x /code/tools/load_init_data.sh
RUN chmod +x /code/tools/run.sh

RUN  /code/tools/install.sh --python python3.11

RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE DATABASE integreat;" && \
    sudo -u postgres psql -c "CREATE USER integreat WITH PASSWORD 'password';" && \
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE integreat TO integreat;" && \
    sudo -u postgres psql -c "ALTER DATABASE integreat OWNER TO integreat;" && \
    sudo -u postgres psql -c "GRANT USAGE, CREATE ON SCHEMA public TO integreat;" && \
    /code/tools/migrate.sh --python python3.11 && \
    /code/tools/load_init_data.sh --python python3.11

# Configure PostgreSQL to allow remote connections
RUN echo "listen_addresses='*'" >> /etc/postgresql/15/main/postgresql.conf && \
    echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/15/main/pg_hba.conf && \
    echo "host all all ::/0 md5" >> /etc/postgresql/15/main/pg_hba.conf

EXPOSE 8000
EXPOSE 5432
CMD service postgresql start && /code/tools/run.sh --python python3.11