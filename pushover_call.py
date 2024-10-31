import socket
import requests
import config

class PushoverCall:
    # @staticmethod
    # def get_public_ip():
    #     try:
    #         response = requests.get('https://api.ipify.org?format=json')
    #         ip_data = response.json()
    #         return ip_data["ip"]
    #     except requests.RequestException as e:
    #         print("Couldn't retrieve IP address:", e)

    @staticmethod
    def get_private_ip():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(('8.8.8.8', 80))
                return s.getsockname()[0]
            except Exception:
                return '127.0.0.1'

    @staticmethod
    def send_push_notification(door_name):
        """Send a push notification with a Yes/No response to close the door."""
        server_ip = PushoverCall.get_private_ip()
        if not server_ip:
            print("Unable to send notification due to missing IP.")
            return
        message = f"The {door_name} has been open for 30 minutes during restricted hours. Close it?"
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": config.PUSHOVER_API_TOKEN,
                "user": config.PUSHOVER_USER_KEY,
                "message": message,
                "title": "Garage Door Monitor",
                "priority": 1,
                "sound": "persistent",
                "url": f"http://{server_ip}:5000/door/close?door_name={door_name}",
                "url_title": "Close Door",
                "retry": 30,
                "expire": 3600,
            }
        )
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print("Failed to send notification:", response.status_code, response.text)