````
git clone git@github.com:w-ays/integreat-cms.git
cd integreat-cms
````

### Setup

To configure your development environment on your system, please follow these steps carefully.

1. Ensure that the following packages are installed alongside your preferred IDE:
   - `npm` version 7 or later
   - `nodejs` version 18 or later
   - `python3` version 3.11 or later
   - `python3-pip` (Debian-based distributions) / `python-pip` (Arch-based distributions)
   - `python3-venv` (only on Debian-based distributions)
   - `gettext` for translation features
   - Either `postgresql` **or** `docker` to run a local database server
   1.1 Using Docker
   ```bash
     docker run --name postgres-integreat -e POSTGRES_USER=integreat -e POSTGRES_PASSWORD=password -e POSTGRES_DB=integreat -p 5432:5432 -d postgres
    ```
    1.2 Using PostgreSQL
    ```bash
    sudo -u postgres psql -c "CREATE USER integreat WITH PASSWORD 'password';"
    sudo -u postgres psql -c "CREATE DATABASE integreat WITH OWNER integreat;"
    ```

2. Run `./tools/install.sh` to download all dependencies.
3. Run `./tools/migrate.sh` to apply all database schema migrations.
4. Run `./tools/load_init_data.sh` to apply init data.
5. Run `./tools/run.sh` to run the development server.
