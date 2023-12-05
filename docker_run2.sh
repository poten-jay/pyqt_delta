#!/usr/bin/env bash

CONTAINER_IMAGE="wimt:pyqt"

USER_VOLUME=""
USER_COMMAND=""
SHARED_FOLDER="/media/ssd/workspace/jay"

# give docker root user X11 permissions
sudo xhost +si:localuser:root

# enable SSH X11 forwarding inside container (https://stackoverflow.com/q/48235040)
XAUTH=/tmp/.docker.xauth
#XAUTH=/tmp
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
sudo chmod 777 $XAUTH

# run the container
sudo docker run --privileged --rm --runtime nvidia --gpus all -it --network host -w /workspace  \
    -e DISPLAY=$DISPLAY \
    -e LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libGLdispatch.so.0 \
    -v /tmp/.X11-unix/:/tmp/.X11-unix \
    -e XAUTHORITY=$XAUTH -v $XAUTH:$XAUTH \
    -v /usr/local/:/usr/local/ \
    -v /dev:/dev \
    -v $SHARED_FOLDER:/workspace \
    $USER_VOLUME $CONTAINER_IMAGE $USER_COMMAND


