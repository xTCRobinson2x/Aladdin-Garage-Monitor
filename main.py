from threading import Thread
from flask_app import app
from monitor import monitor_door,test_pushover_notification

if __name__ == "__main__":
    
    # monitor_door()
    # monitor_thread = Thread(target=monitor_door, daemon=True)
    monitor_thread = Thread(target=test_pushover_notification, daemon=True)
    monitor_thread.start()

    app.run(host='0.0.0.0', port=5000)