#!/bin/sh

cd server/master
docker build -t masterslurm .
cd ../node
docker build -t nodeslurm .
