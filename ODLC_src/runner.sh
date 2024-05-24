#!/bin/bash

for i in {1..5}; do
    docker-compose up
    sleep 5
done
