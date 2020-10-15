#!/usr/bin/env bash

COURSE_ROOT_DIR=/test-course
COURSE_REPO_NAME=test-cpp-course

COURSE_DEFAULT_START_DIR=$COURSE_ROOT_DIR/$COURSE_REPO_NAME

if [[ $EUID == 0 ]]; then
   echo "This script must be run as non-root user inside docker group"
   exit 1
fi

if [[ -z $course_docker_start_directory ]]; then
    course_docker_start_directory=$COURSE_DEFAULT_START_DIR
fi

docker exec -it --user $(id -u):$(id -g) tpcc-image /bin/bash -c \
"if [[ -d $course_docker_start_directory ]]; then
    cd $course_docker_start_directory
fi
/bin/bash"

