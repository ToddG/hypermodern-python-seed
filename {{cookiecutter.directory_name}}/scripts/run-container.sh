#!/bin/bash

# run this from project root directory

# run arbitrary command within docker container
docker run {{cookiecutter.project_name}}-build-container:latest \
    -v .:/project -w /project $*

