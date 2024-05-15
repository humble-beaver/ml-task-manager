# Machine Learning Task Manager

The goal of the project is to build a dockerized service that will accept HTTPS requests with a JSON payload containing information about a new ML task that must be sent to the cluster. This JSON will contain the information described bellow, followed by another payload with the running script. The API server will be a FastAPI python server, connected to a PostgreSQL database.

## Application Stack

This is the stack of technologies used in this application:

- FastAPI
- PostgreSQL
- Docker
- SQLModel

## Task Request Model

The JSON file sent with the request must contain the following fields:

1. TBD

## Installing and Running

We can build and run the developing system by calling the following single command:

```bash
docker-compose up -d --build
```

For the production environment, we can run

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

By doing so, docker will build the image and spin up the two containers in dettached mode, i.e. silently in the background. We can then go to localhost:8008/docs (for the dev container) and localhost:8009/docs for the prod container, in order to access the builtin API documentaion.

For monitoring and checking for errors, you can acompany the logs by issuing `docker-compose logs -f`.

If you must rebuild or restart the hole process, you can bring down the containers and the associated volumes with:

```bash
docker-compose down -v  # dev
docker-compose -f docker-compose.prod.yml down -v  # prod
```

### Sanity checks

To assure if it is all running correctly, we can connect to the database command prompt and list databases and relations

```bash
$ docker-compose exec db psql --username=ml-task-manager --dbname=ml-task-manager

psql (15.1)
Type "help" for help.

ml-task-manager=# \l

Name       |      Owner      | Encoding |  Collate   |   Ctype    | ICU Locale | Locale Provider |            Access privileges            
-----------------+-----------------+----------+------------+------------+------------+-----------------+-----------------------------------------
 ml-task-manager | ml-task-manager | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
 postgres        | ml-task-manager | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | 
 template0       | ml-task-manager | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/"ml-task-manager"                   +
                 |                 |          |            |            |            |                 | "ml-task-manager"=CTc/"ml-task-manager"
 template1       | ml-task-manager | UTF8     | en_US.utf8 | en_US.utf8 |            | libc            | =c/"ml-task-manager"                   +
                 |                 |          |            |            |            |                 | "ml-task-manager"=CTc/"ml-task-manager"
(4 rows)

ml-task-manager=# \c ml-task-manager

You are now connected to database "ml-task-manager" as user "ml-task-manager".

ml-task-manager=# \dt

# May be different initially, if you don't have any task created
            List of relations
 Schema | Name | Type  |      Owner      
--------+------+-------+-----------------
 public | task | table | ml-task-manager
(1 row)

ml-task-manager=# \q
```

We can also check that the volume was created as well by running:

```bash
docker volume inspect ml-task-manager_postgres_data
```

You will get something like this:

```bash
[
    {
        "CreatedAt": "2024-04-01T09:54:45-03:00",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "ml-task-manager",
            "com.docker.compose.version": "2.24.7",
            "com.docker.compose.volume": "postgres_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/ml-task-manager_postgres_data/_data",
        "Name": "ml-task-manager_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```
