# Project Description

**Project Name**: dbt Data Pipeline with PostgreSQL and Docker

## Overview:

This project is a robust data engineering pipeline built to showcase the integration of dbt (data build tool) with PostgreSQL for data transformation, versioning, and testing. The setup leverages Docker for containerized deployment, ensuring an isolated and reproducible environment.

This project is designed to provide a scalable, flexible, and automated solution for loading, transforming, and managing data efficiently.

## Key Components:

- **PostgreSQL Database**: Stores raw and transformed data, serving as the data warehouse and supporting snapshots, transformations, and tests through dbt.

- **dbt (Data Build Tool)**: Performs data transformations, quality checks, and manages schema changes, leveraging a modular SQL approach to structure and version data processing tasks.

- **Docker and Docker Compose**: Encapsulates the dbt and PostgreSQL services, ensuring consistent setup across environments, along with network isolation for secure data management.

**Environment Configuration with .env Files**: Uses environment variables to securely manage credentials and configurations across different services, simplifying deployment and maintenance.

# DBT Project Setup Guide

This project is a demonstration of dbt Data Pipeline with PostgreSQL and Docker

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker (version 20.10.0 or higher)
- Git (version 2.0 or higher)
- Python (version 3.11 or higher)

## Quick Start

Clone the git repo as shown below:

```bash
git clone https://github.com/scriptstar/dbt_pg_project.git
cd dbt_pg_project
```

> Note: Create a `.env` file in the project root directory and add the following content:

```bash
# feel free to change the values
DB_USER=dbtuser
DB_PASSWORD=dbt123Abc
DB_DATABASE=dbtpg
DB_HOST=postgres
DB_PORT=5432
```

1. Start the containers:

> Note: make sure your docker is up and running

```bash
docker compose up -d --build
```

> Note: Make sure to configure your database connection in `profiles.yml` before running dbt commands.

2. Access the dbt container:

```bash
docker exec -it dbt_core /bin/bash
```

3. Run dbt commands:

```bash
# Install dependencies and set up the project
dbt deps

# Build your dbt project
dbt clean                     # Clean the target directory
dbt snapshot                  # Run snapshots
dbt run                      # Run models
dbt test                     # Run tests

# Generate and view documentation
dbt docs generate
dbt docs serve --port 8080 --host 0.0.0.0
```

The documentation will be available at http://localhost:3000

4. Create snapshots

> Note: make sure you are in the `dbt_core` container (or `make sh`)

Run the `update_data.py` script to update a few records in the customer table:

```bash
python /usr/app/dbt_project/database/scripts/update_data.py
```

The above script uses `SQLAlchemy` to make changes to the `customer` data in the postgres database.

Run snapshot and create models again.

```bash
dbt snapshot
dbt run
```

Let's verify the updated customer records using `psql`

```bash
# connect to the Postgres
psql -h dbt_postgres -U dbtuser -d dbtpg
```

You need to provide the password

```bash
# check your .env file for the password for the user dbtuser
Password for user dbtuser:
```

Once you connected to the Postgres then run the following select statment

```sql
select * from snapshots.customers_snapshot where customer_id = 82;
```

Output: You must see two rows.

```bash
 customer_id | zipcode |     city     | state_code |  datetime_created   |  datetime_updated   |            dbt_
scd_id            |   dbt_updated_at    |   dbt_valid_from    |    dbt_valid_to
-------------+---------+--------------+------------+---------------------+---------------------+----------------
------------------+---------------------+---------------------+---------------------
          82 |   59655 | areia branca | RN         | 2017-10-18 00:00:00 | 2017-10-18 00:00:00 | d5ce49419bd8ed8
44a90e39c381a96d3 | 2017-10-18 00:00:00 | 2017-10-18 00:00:00 | 2017-10-18 00:10:00
          82 |   24120 | niteroi      | RJ         | 2017-10-18 00:00:00 | 2017-10-18 00:10:00 | 795e83e8b873e55
d2443643dae7b1db0 | 2017-10-18 00:10:00 | 2017-10-18 00:10:00 |
(2 rows)
```

You can see customer updates are propagated to the snapshot table and we demonstrated **Slowly Changing Dimensions** (SCD2) approach in dbt.

Press `q` to exit the `psql` prompt

## Makefile Commands

The project includes a Makefile that provides convenient commands for managing the Docker containers. Here are the available commands:

- `make build`: Builds the Docker images for the project.
- `make docker-up`: Starts the Docker containers.
- `make up`: Runs `make build` followed by `make docker-up`.
- `make down`: Stops and removes the Docker containers.
- `make volumes`: Lists all the Docker volumes.
- `make restart`: Stops the containers, removes the volumes, and starts the project again from scratch.
- `make sh`: Opens a shell inside the `dbt_core` container.

You can run these commands from the project root directory. For example, to start the project, you can use:

```bash
make up
```

This will build the Docker images and start the containers. The other Makefile commands provide a convenient way to manage the project's Docker environment without having to remember the exact Docker Compose commands.

## Common Commands

### Exit the container

```bash
exit
```

### Stop and remove containers

```bash
docker compose down
```

## Project Structure

```
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── logs
├── dbt_project/
│   ├── models/
│   ├── profiles.yml
│   ├── snapshots/
│   ├── tests/
│   └── dbt_project.yml
├── raw_data/
└── requirements.txt
```

## Troubleshooting

If you can't access the dbt docs, ensure:

- The container is running (`docker ps`)
- You're using the correct port (3000)
- You've generated the docs before serving
- The docs server is running with `--host 0.0.0.0` flag

For container issues:

```bash
# Rebuild containers
docker compose down
docker compose up -d --build

# Check container logs
docker logs dbt_core
docker logs pg_init_data_load
```
