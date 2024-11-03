#!/bin/bash

APP_USER="aladdin_monitor"
APP_DIR="/opt/aladdin_garage_monitor"
SERVICE_FILE="/etc/systemd/system/aladdin_garage_monitor.service"
BUILD_FILE="main"
MAIN_PY="main.py"
LOG_FILE="/var/log/aladdin_garage_monitor.log"

if [ -d "venv" ]; then
    echo "Removing existing virtual environment"
    rm -rf venv
fi

# Install necessary packages
echo "Installing necessary packages..."
sudo apt update && sudo apt install -y python3 python3-venv || { echo "Package installation failed"; exit 1; }

# Create application user if it doesn't already exist
if ! id -u "$APP_USER" > /dev/null 2>&1; then
    echo "Creating application user..."
    sudo useradd -r -s /bin/false "$APP_USER"
fi

# Create application directory if it doesn't already exist
if [ ! -d "$APP_DIR" ]; then
    echo "Setting up application directory..."
    sudo mkdir -p "$APP_DIR"
    sudo chown "$APP_USER":"$APP_USER" "$APP_DIR"
fi

# Set up Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt || { echo "Python dependencies installation failed"; exit 1; }
fi

# Build app
if [ ! -f "$APP_DIR/$BUILD_FILE" ]; then
    echo "Building app file for service"
    pyinstaller --onefile $MAIN_PY
    cp dist/$BUILD_FILE $APP_DIR/$BUILD_FILE
fi

# Create the log file with appropriate permissions
if [ ! -f "$LOG_FILE" ]; then
    echo "Creating log file..."
    sudo touch "$LOG_FILE"
    sudo chown "$APP_USER":"$APP_USER" "$LOG_FILE"
    sudo chmod 644 "$LOG_FILE"
fi

# Create systemd service file
echo "Creating systemd service file..."
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Garage Door Monitor Service
After=network.target

[Service]
ExecStart=$APP_DIR/$BUILD_FILE
WorkingDirectory=$APP_DIR
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE
Restart=always
User=$APP_USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL


# Reload systemd, enable, and start the service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable aladdin_garage_monitor.service
sudo systemctl restart aladdin_garage_monitor.service

echo "Installation complete. Check the service status with: sudo systemctl status aladdin_garage_monitor.service"
