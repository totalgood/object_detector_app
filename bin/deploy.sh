#!/usr/bin/env bash

git pull origin master

/bin/bash ./bin/update_env.sh

/bin/bash ./bin/run.sh &