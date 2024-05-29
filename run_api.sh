#!/bin/bash

echo $FOLDER
cd $FOLDER
uvicorn app.main:app --port 8008 --host 0.0.0.0
