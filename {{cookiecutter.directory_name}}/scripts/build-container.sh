#!/bin/bash

# run this from project root directory

# build docker container
docker build docker/. -t {{cookiecutter.project_name}}-build-container:latest
