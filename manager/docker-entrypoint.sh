#!/bin/bash

sudo service munge start

/usr/bin/sshd -D
