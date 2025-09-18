#!/bin/bash
set -e

# Start SSH server in the background
/usr/sbin/sshd

# Start Apache in foreground to keep container running
exec apache2ctl -D FOREGROUND
