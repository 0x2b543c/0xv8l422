#!/bin/bash

docker run -p 8080:8080 -v "${PWD}:/workspace" coinmetrics/tooling:latest 
