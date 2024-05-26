#!/bin/bash

echo "Building Instrument Cluster Python Application"

podman build -t instrumentcluster -f Dockerfile
 
