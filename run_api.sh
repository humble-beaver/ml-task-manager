#!/bin/bash

while !</dev/tcp/db/5432; do sleep 1; done; uvicorn app.main:app --port 8008 --host 0.0.0.0
