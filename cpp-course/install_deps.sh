#!/bin/sh

set -e -x

apt-get update

DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

apt-get install -y \
	ssh \
	make \
	cmake \
	ninja-build \
	git \
	clang-10 \
	clang-format-10 \
	clang-tidy-10 \
	lldb-10 \
	python3 \
	python3-pip \
	python3-venv \
	ca-certificates \
	openssh-server \
	rsync \
	vim \
	gdb \
	wget \
	autoconf \
	iputils-ping \
	binutils-dev

pip3 install \
	click \
	gitpython \
	python-gitlab \
	termcolor \
	virtualenv \
	argcomplete
