#!/bin/bash

cd ml-task-manager
uvicorn app.main:app --port 8008 --host 0.0.0.0
