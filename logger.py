import os
import platform
import logging

def logger():
    if os.name == 'nt':  # Windows
            log_file_path = r'C:\logs\aladdin_garage_monitor.log'
            log_dir = os.path.dirname(log_file_path)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
    elif platform.system() == 'Darwin':  # macOS
            log_file_path = '/usr/local/var/log/aladdin_garage_monitor.log'
    else:  # Linux or other Unix-like systems
            log_file_path = '/var/log/aladdin_garage_monitor.log'

    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    return logging.getLogger("aladdin_garage_monitor")