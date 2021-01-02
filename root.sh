#!/usr/bin/env bash

COURSE_CONTAINER=test-cpp-course

if [[ $EUID == 0 ]]; then
   echo "This script must be run as non-root user inside docker group"
   exit 1
fi

docker exec -it --user root $COURSE_CONTAINER /bin/bash --rcfile /bashrc
