# ----------------------------------------------------------------------------
# build container based on ubuntu
# ----------------------------------------------------------------------------
FROM ubuntu:20.04 as base_0

# configure unattended installation
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# update base image
RUN apt-get update && apt-get upgrade

# install tzdata as sometimes it asks for user input
RUN truncate -s0 /tmp/timzone.cfg &&                                        \
   (echo "tzdata tzdata/Areas select America" >> /tmp/timzone.cfg) &&       \
   (echo "tzdata tzdata/Zones/America select Los_Angeles"                   \
   >> /tmp/timzone.cfg) &&                                                  \
   debconf-set-selections /tmp/timzone.cfg &&                               \
   rm -f /etc/timezone /etc/localtime &&                                    \
   apt-get install -y tzdata apt-utils software-properties-common gcc
RUN rm -rf /tmp/*

# ----------------------------------------------------------------------------
# install python, pip, virtualenv and dependencies
# ----------------------------------------------------------------------------
FROM base_0 as base_1

RUN apt-get update -y &&                                                    \
    apt-get install -y python3 python3-venv python3-distutils               \
    python3-lib2to3 python3-pip python3-apt dvipng latexmk curl wget git    \
    build-essential 

# ----------------------------------------------------------------------------
# install homebrew as that is the easiest way to install dependencies 
# ----------------------------------------------------------------------------
FROM base_1 as base_2
# from https://stackoverflow.com/questions/58292862/how-to-install-\
# homebrew-on-ubuntu-inside-docker-container
RUN useradd -m -s /bin/zsh linuxbrew && \
    usermod -aG sudo linuxbrew &&  \
    mkdir -p /home/linuxbrew/.linuxbrew && \
    chown -R linuxbrew: /home/linuxbrew/.linuxbrew
USER linuxbrew
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
USER root
RUN chown -R $CONTAINER_USER: /home/linuxbrew/.linuxbrew


# ----------------------------------------------------------------------------
# install poetry, nox, and other build dependencies 
# ----------------------------------------------------------------------------
RUN echo 'PATH=$PATH:/home/linuxbrew/.linuxbrew/bin' >> /root/.bash_aliases 
RUN /home/linuxbrew/.linuxbrew/bin/brew install gcc nox poetry
COPY ./launcher.sh /launcher.sh 

ENTRYPOINT ["/launcher.sh", "nox"]
