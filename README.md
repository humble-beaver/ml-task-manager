# Machine Learning Task Manager

The goal of the project is to build a dockerized service that will accept HTTPS requests with a JSON payload containing information about a new ML task that must be sent to the cluster. This JSON will contain the information described bellow, followed by another payload with the running script. The API server will be a FastAPI python server, connected to a PostgreSQL database.

## Application Stack

This is the stack of technologies used in this application:

- FastAPI
- PostgreSQL
- Docker

## Task Request Model

The JSON file sent with the request must contain the following fields:

1. TODO...
