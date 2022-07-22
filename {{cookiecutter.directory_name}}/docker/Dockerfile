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
RUN apt-get install -y python3 python3-venv python3-distutils               \
    python3-lib2to3 python3-pip python3-apt dvipng latexmk curl wget git    \
    gcc build-essential

# ----------------------------------------------------------------------------
# install poetry, nox, and other build dependencies 
# ----------------------------------------------------------------------------
FROM base_2 as base_3
RUN pip install nox poetry

# misc stuff
RUN apt-get install -y vim

# ----------------------------------------------------------------------------
# entrypoint
# ----------------------------------------------------------------------------
COPY ./launcher.sh /launcher.sh
ENTRYPOINT ["/launcher.sh", "nox"]
