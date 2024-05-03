#!/bin/sh

$CONTAINER_NAME = $1

docker inspect $CONTAINER_NAME | grep IPAddress
