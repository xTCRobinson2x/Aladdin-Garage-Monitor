#!/bin/bash

APP_USER="aladdin_monitor"
APP_DIR="/opt/aladdin_garage_monitor"
SERVICE_FILE="/etc/systemd/system/aladdin_garage_monitor.service"
LOG_FILE="/var/log/aladdin_garage_monitor.log"

# Stop and disable the service
echo "Stopping and disabling the service..."
if sudo systemctl is-active --quiet aladdin_garage_monitor.service; then
    sudo systemctl stop aladdin_garage_monitor.service
fi
sudo systemctl disable aladdin_garage_monitor.service

# Remove the systemd service file
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing the systemd service file..."
    sudo rm -f "$SERVICE_FILE"
else
    echo "Service file not found, skipping removal."
fi

# Reload systemd to apply changes
echo "Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl reset-failed

# Remove the application directory
if [ -d "$APP_DIR" ]; then
    echo "Removing the application directory..."
    sudo rm -rf "$APP_DIR"
else
    echo "Application directory not found, skipping removal."
fi

# Remove the log file
if [ -f "$LOG_FILE" ]; then
    echo "Removing the log file..."
    sudo rm -f "$LOG_FILE"
else
    echo "Log file not found, skipping removal."
fi

# Remove the application user if it exists
if id "$APP_USER" &>/dev/null; then
    echo "Removing the application user..."
    sudo userdel -r "$APP_USER"
else
    echo "User $APP_USER does not exist, skipping removal."
fi

echo "Uninstallation complete."
