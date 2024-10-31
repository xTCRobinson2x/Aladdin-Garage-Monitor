import datetime
import time
import config
from aladdin_connect import AladdinConnect
from logger import logger
from pushover_call import PushoverCall

log = logger()


def monitor_door():
    global aladdin
    global doors
    username = config.ALADDIN_USERNAME
    password = config.ALADDIN_PASSWORD
    
    aladdin = AladdinConnect(username, password)
    last_opened = None

    log.info(f"Starting monitoring")

    while True:
        doors = aladdin.get_all_doors()
        now = datetime.datetime.now()
        for door in doors:
            door_status = aladdin.DoorStatus.get(door['status'])
            log.info(f"{now} - {door['name']} is {door_status}")
            
            if door_status == 'OPEN':
                if last_opened == None:
                    last_opened = now
                    log.info(f"{now} - {door['name']} last opened {last_opened}")

                elif (now - last_opened).seconds >= 1200 and (now.hour >= 22 or now.hour < 6):
                    PushoverCall.send_push_notification(door['name'])
                    log.info(f"{now} - Sent notification to close door")
                    time.sleep(1200)
  
                elif (last_opened and (now.hour >= 22 or now.hour <= 6)):
                    log.info(f"{now} - {door['name']} last opened {last_opened}")                
                    
            else:
                last_opened = None
            
        time.sleep(5)

def test_pushover_notification():

    global aladdin
    global doors
    username = config.ALADDIN_USERNAME
    password = config.ALADDIN_PASSWORD
    
    aladdin = AladdinConnect(username, password)
    last_opened = None

    print(f"Starting monitoring")

    while True:
        doors = aladdin.get_all_doors()
        now = datetime.datetime.now()
        for door in doors:
            door_status = aladdin.DoorStatus.get(door['status'])
            print(f"{now} - {door['name']} is {door_status}")
            
            if door_status == 'CLOSED':
                if last_opened == None:
                    last_opened = now
                    print(f"{now} - {door['name']} last opened {last_opened}")
                elif (now - last_opened).seconds >= 10 and (now.hour >= 19 or now.hour < 6):
                    PushoverCall.send_push_notification(door['name'])
                    print(f"{now} - Sent notification to close door")
                    time.sleep(120)
  
                elif (last_opened and (now.hour >= 19 or now.hour < 6)):
                    print(f"{now} - {door['name']} last opened {last_opened}")
                print(f"{now} - {door['name']} is {door_status}")
                
                    
            else:
                last_opened = None
                print(f"{now} - {door['name']} is {door_status}")
            
        time.sleep(5)

def close_door_action(given_door_name):
    global doors, aladdin
    for door in doors:
        if door['name'] == given_door_name:
            try:
                aladdin.set_door_status(door, aladdin.DesiredDoorStatus['CLOSE'])
                return f"{given_door_name} is now closing", 200
            except Exception as e:
                log.error(f"\nFailed to close door {given_door_name}: {str(e)}")
                return f"{str(e)}", 202
    return "Door not found", 404

