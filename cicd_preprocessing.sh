#!/usr/bin/env bash

IMAGE_NAME="laetus/pen-collected-items-preprocessing"


# get last commit hash prepended with @ (i.e. @8a323d0)
function parse_git_hash() {
  git rev-parse HEAD 2> /dev/null
}

# DEMO
GIT_COMMIT=$(parse_git_hash)

echo $GIT_COMMIT

sudo docker build -t "$IMAGE_NAME:test" -f Dockerfile_preprocessing .

sudo docker tag "$IMAGE_NAME:test" "$IMAGE_NAME:$GIT_COMMIT"

sudo docker tag "$IMAGE_NAME:test" "$IMAGE_NAME:latest" 

sudo docker push "$IMAGE_NAME:$GIT_COMMIT" 
sudo docker push "$IMAGE_NAME:latest" 