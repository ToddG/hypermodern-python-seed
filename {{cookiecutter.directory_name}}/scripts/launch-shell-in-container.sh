#!/bin/bash

# run this from project root directory

# launch bash inside docker container
docker run  -p 127.0.0.1:80:8080 -v `(pwd)`:/project -u `id -u`:`id -g` -w /project --entrypoint /bin/bash -it {{cookiecutter.project_name}}-build-container:latest

