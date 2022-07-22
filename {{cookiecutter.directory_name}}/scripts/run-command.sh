#!/bin/bash

# run this from project root directory

# run arbitrary command within docker container
docker run -v `(pwd)`:/project -u `id -u`:`id -g` -w /project -it {{cookiecutter.project_name}}-build-container:latest $*

