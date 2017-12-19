#!/usr/bin/env bash


source activate object-detection

python object_detection_app.py -u=rtsp://52.39.224.108:1935/live/myStream &>> log.txt