#!/bin/bash

echo "This installation file should work for:"
echo "  - Debian based distros (Ubuntu, Pop_OS!, ...)"
echo "  - Arch-based distros (Arch, Manjaro, ...)"
echo "  - Fedora"

# dnf needs to be first because Fedora also has yum
if [[ ! -z $(which dnf) ]]; then
    PKM=dnf
elif [[ ! -z $(which yum) ]]; then
    PKM=yum
elif [[ ! -z $(which apt-get) ]]; then
    PKM=apt-get
elif [[ ! -z $(which pamac) ]]; then
    PKM=pamac
fi

echo "Using package manager: $PKM"

# Install ansible
echo "sudo $PKM install ansible"
sudo $PKM install -y ansible

# Run ansible playbook
ansible-playbook general.yml --ask-become-pass