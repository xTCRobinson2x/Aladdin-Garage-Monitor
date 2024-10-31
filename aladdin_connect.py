import requests
import hmac
import hashlib
import base64
import json

class AladdinConnect:
    AUTH_HOST = 'https://cognito-idp.us-east-2.amazonaws.com/'
    AUTH_CLIENT_ID = '27iic8c3bvslqngl3hso83t74b'
    AUTH_CLIENT_SECRET = '7bokto0ep96055k42fnrmuth84k7jdcjablestb7j53o8lp63v5'
    API_HOST = 'https://api.smartgarage.systems'

    DoorStatus = {
        0: 'UNKNOWN',
        1: 'OPEN',
        2: 'OPENING',
        3: 'TIMEOUT_OPENING',
        4: 'CLOSED',
        5: 'CLOSING',
        6: 'TIMEOUT_CLOSING',
        7: 'NOT_CONFIGURED'
    }

    DesiredDoorStatus = {
        'CLOSE': 0,
        'OPEN': 1,
        'NONE': 99
    }
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = None
    
    def get_secret_hash(self, message, key):
        dig = hmac.new(key.encode('utf-8'), msg=message.encode('utf-8'), digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()
    
    def get_access_token(self):
        auth_parameters = {
            'USERNAME': self.username,
            'PASSWORD': self.password,
            'SECRET_HASH': self.get_secret_hash(self.username + self.AUTH_CLIENT_ID, self.AUTH_CLIENT_SECRET)
        }

        payload = {
            'ClientId': self.AUTH_CLIENT_ID,
            'AuthFlow': 'USER_PASSWORD_AUTH',
            'AuthParameters': auth_parameters
        }

        headers = {
            'Content-Type': 'application/x-amz-json-1.1',
            'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
        }

        response = requests.post(self.AUTH_HOST, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            self.access_token = response.json()['AuthenticationResult']['AccessToken']
        else:
            raise Exception(f"Error getting access token: {response.status_code} {response.text}")
    
    def get_all_doors(self):
        if not self.access_token:
            self.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.get(f'{self.API_HOST}/devices', headers=headers)

        if response.status_code == 200:
            devices = response.json()['devices']
            doors = []
            for device in devices:
                for door in device['doors']:
                    door_info = {
                        'deviceId': device['id'],
                        'id': door['id'],
                        'index': door['door_index'],
                        'serialNumber': device['serial_number'],
                        'name': door.get('name', 'Garage Door'),
                        'status': door.get('status', 'UNKNOWN'),
                        'batteryLevel': door.get('battery_level', 0),
                        'fault': door.get('fault', False)
                    }
                    doors.append(door_info)
            return doors
        else:
            raise Exception(f"Error getting doors: {response.status_code} {response.text}")

    def set_door_status(self, door, desired_status):
        if not self.access_token:
            self.get_access_token()
        
        command = 'OPEN_DOOR' if desired_status == self.DesiredDoorStatus['OPEN'] else 'CLOSE_DOOR'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'command': command
        }

        response = requests.post(
            f"{self.API_HOST}/command/devices/{door['deviceId']}/doors/{door['index']}", 
            headers=headers, 
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            print(f"Door {door['name']} command {command} was successful.")
        else:
            #raise Exception(f"Error setting door status: {response.status_code} {response.text}")
            raise Exception(f"{json.loads(response.text).get('error')}")