#!/usr/bin/env bash

COURSE_CONTAINER=test-cpp-course

docker container stop $COURSE_CONTAINER
docker container rm $COURSE_CONTAINER
