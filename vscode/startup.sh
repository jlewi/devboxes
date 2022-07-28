#!/bin/bash
set -ex

# If the home directory doesn't exist create
# TODO(jeremy): Should we also create a .bash_profile
if [ ! -d ${HOME} ]; then
	mkdir -p ${HOME}
fi

# Create the hostkey
# N.B. In principle this key doesn't have to be different from the ssh key
# used with GitHub and arguably should be the same key. We just chose
# to generate a new key because it was easier to do it this way and
# keep it in sync with the value in sshd_config.
if [ ! -f ${HOME}/.ssh/host_key ]; then
	mkdir -p ${HOME}/.ssh
	ssh-keygen -t ed25519 -N "" -f ${HOME}/.ssh/host_key
fi

# Add the authorized ssh key
if [ ! -f ${HOME}/.ssh/authorized_keys ]; then
	cp /authorized_keys/authorized_keys ${HOME}/.ssh/authorized_keys 
fi

# Copying the secrets is easier then dealing with ssh-agent
# With ssh agent we would need to add the commands to set SSH_AGENT_PID and SSH_AUTH_SOCK
# to our bash profile so that ever shell we have has them set
cp /secrets/id_ed25519* ${HOME}/.ssh/

chmod 0700 ${HOME}
chmod 0700 ${HOME}/.ssh/
chmod 0600 ${HOME}/.ssh/authorized_keys

# Start supervisor this will run forever which will prevent
# the container from terminating which is desired.
# supervisor will run the ssh server
supervisord -c /etc/supervisord.conf