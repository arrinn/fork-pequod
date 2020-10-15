#!/usr/bin/env bash

COURSE_IMAGE=test-course-image

docker container stop $COURSE_IMAGE
docker container rm $COURSE_IMAGE

