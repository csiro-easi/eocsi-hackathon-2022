#!/usr/bin/env bash

# Create and configure a new virtual env to run WOfS within EASI

venv=wofs
venv_name="WOfS Environment"
venv_root=~/.venv
script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
repos_dir=${script_dir}/../..

function create_venv() {
    # Create a virtual env if not already there
    if ! $(jupyter kernelspec list | grep -q ${venv}); then
        echo "Creating virtual env. Please wait..."
        mkdir -p ${venv_root}
        python -m venv ${venv_root}/${venv}
        realpath /env/lib/python3.8/site-packages > ${venv_root}/${venv}/lib/python3.8/site-packages/base_venv.pth
        source ${venv_root}/${venv}/bin/activate
        python -m ipykernel install --user --name=${venv} --display-name "${venv_name}"
        deactivate
    fi
}

function install_dependencies() {
    # Install WOfS python dependencies
    echo "Creating/updating python dependencies. Please wait..."
    source ${venv_root}/${venv}/bin/activate
    pip install -U ephem
    pip install -U --index-url https://packages.dea.ga.gov.au/ wofs
    deactivate
}

if [ -d ${venv_root}/${venv} ]; then
    echo "${venv_name} kernel already installed"
else
    create_venv
    install_dependencies
fi
