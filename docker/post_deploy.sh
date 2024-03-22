#! /bin/sh

set -e  # Stop the script if it returns an error code
set -u  # Stop the script if some variable is not defined
set -x  # Display each command before executing it

umask 000 # Setting broad permissions to share log volume