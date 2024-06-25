#!/bin/bash

# Define where to install
INSTALL_DIR="/usr/local/bin"
SCRIPT="kmerge.py"
EXECUTABLE="kmerge"

# Check if running as root, otherwise suggest running as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Copy the script to /usr/local/bin and rename it
cp $SCRIPT $INSTALL_DIR/$EXECUTABLE

# Make the script executable
chmod +x $INSTALL_DIR/$EXECUTABLE

echo "Installation completed. You can now use 'kmerge' command."