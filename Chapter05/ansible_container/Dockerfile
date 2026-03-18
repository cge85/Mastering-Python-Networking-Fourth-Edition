# Getting base image
FROM ubuntu:22.04
# No need for interactive prompt
ENV DEBIAN_FRONTEND=noninteractive
# Run any command, i.e. install packages
RUN apt update && apt install -y python3.10 python3-pip ansible vim
RUN pip install ansible-pylibssh
# specify a working directory
WORKDIR /app
COPY . /app
