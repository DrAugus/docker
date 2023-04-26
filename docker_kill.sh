#!/bin/bash

rm_docker() {

    # echo "!!! do not kill now !!!" && exit 0

    # kill rm exist
    echo -e "# kill rm exist\n"
    rm_id=$(docker ps -a | grep "$1" | cut -d ' ' -f 1)
    rm_arr=(${rm_id// /})
    echo "need kill dockers are: ${rm_arr[@]}"
    for id in ${rm_arr[@]}
    do
        # echo ">>> rm id $id"
        echo -e "> kill\n"
        docker kill $id
        echo -e "> rm\n"
        docker rm $id
    done
}
