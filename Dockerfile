FROM ubuntu:16.04

LABEL maintainer="Aarya Bhosale <aaryaa.bhosale@infobeans.com>"
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        build-essential \
        python-dev \
        python-pip \
        curl \
        git \
        python-setuptools \
        sudo \
        && rm -rf /var/lib/apt/lists/*


RUN  sudo pip install virtualenv

