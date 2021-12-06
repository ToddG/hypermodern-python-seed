#!/bin/bash

# run this from project root directory

# launch bash inside docker container
docker run -v `(pwd)`:/project -w /project --entrypoint /bin/bash -it {{cookiecutter.project_name}}-build-container:latest

