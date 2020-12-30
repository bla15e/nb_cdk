#!/bin/sh
# Use this to install software packages

# Install Conda
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p
rm ~/miniconda.sh
source $HOME/miniconda3/bin/activate

# Install vs-code-server

# Configure vs-code-server