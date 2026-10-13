#!/bin/bash


#conda init
#conda activate shtick

jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --ServerApp.root_dir="/Users/chran/repo/shtick" \
    --IdentityProvider.token="pt"
