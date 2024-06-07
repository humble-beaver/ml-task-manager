#!/bin/bash

export DATABASE_URL=ANY
uvicorn app.main:app --reload
