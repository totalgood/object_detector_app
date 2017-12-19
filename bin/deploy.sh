#!/usr/bin/env bash

git pull origin master

/bin/bash ./bin/update_env.sh

date &>> pids.txt
/bin/bash ./bin/run.sh &
$! &>> pids.txt