#!/bin/bash

print_usage(){
    echo "Usage: $0 [NAME]"
}

if [ $# -lt 1 ]; then
    print_usage
    exit 1
fi

. ./docker_kill.sh

run_name=""
docker_name=""

. ./ffmpeg.sh

if [ "$1" = "ffmpeg" ] 
then
    rm_docker $run_name
    run_name=ffmpeg_demo
    docker_name=jrottenberg/ffmpeg
    docker run -it \
        --name ${run_name} \
        ${docker_name}:latest split_video
    exit 0
fi




