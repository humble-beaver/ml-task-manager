#!/bin/sh

cd ../app
docker build -t ml-task-manager .

cd ../manager
docker build -t managerslurm .

cd ../server/master
docker build -t masterslurm .

cd ../node
docker build -t nodeslurm .