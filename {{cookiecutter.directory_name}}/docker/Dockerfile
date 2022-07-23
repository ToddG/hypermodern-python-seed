# ----------------------------------------------------------------------------
# build container based on ubuntu
# ----------------------------------------------------------------------------
FROM ubuntu:20.04 as base_0

# configure unattended installation
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# upgrade base image
RUN apt-get update -y && apt-get upgrade -y


# ----------------------------------------------------------------------------
# install tzdata as sometimes it asks for user input
# ----------------------------------------------------------------------------
FROM base_0 as base_1
RUN truncate -s0 /tmp/timzone.cfg &&                                        \
   (echo "tzdata tzdata/Areas select America" >> /tmp/timzone.cfg) &&       \
   (echo "tzdata tzdata/Zones/America select Los_Angeles"                   \
   >> /tmp/timzone.cfg) &&                                                  \
   debconf-set-selections /tmp/timzone.cfg &&                               \
   rm -f /etc/timezone /etc/localtime &&                                    \
   apt-get install -y tzdata apt-utils software-properties-common
RUN rm -rf /tmp/*

# ----------------------------------------------------------------------------
# install dev tools
# ----------------------------------------------------------------------------
FROM base_1 as base_2
RUN add-apt-repository -y ppa:deadsnakes/ppa &&                             \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils      \
    python3.10-dev python3.10-lib2to3                                       \
    dvipng latexmk curl wget git                                            \
    gcc build-essential vim

RUN apt-get remove -y python3.8 &&                                          \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 10

RUN python -m ensurepip && python -m pip install -U pip

# ----------------------------------------------------------------------------
# install poetry, nox, and other build dependencies 
# ----------------------------------------------------------------------------
FROM base_2 as base_3
RUN pip install nox poetry

# ----------------------------------------------------------------------------
# entrypoint
# ----------------------------------------------------------------------------
COPY ./launcher.sh /launcher.sh
ENTRYPOINT ["/launcher.sh", "nox"]
