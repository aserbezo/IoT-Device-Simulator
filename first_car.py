import time
from dotenv import load_dotenv
from function import Functions
import os
from datetime import datetime
import random
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import json

random.seed(50)
load_dotenv()


class FirstCar():
    # Access the environment variable
    CONN_STRING = os.getenv('first_car_connection_string')
    ALERT = ['Brake Detection', 'Battery Charge Warning Light', 'Oil Pressure Warning Light', 'Brake Warning Light',
             'Transmission Temperature', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None',
             'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']
    #  Normal 30 to 35 PSI
    TIRE_PRESURE = [30, 31, 32, 33, 29, 25]
    # between 75 to 105 degrees Celsius
    SPEED = [60, 64, 65, 68, 70, 75, 77, 74, 80, 82, 88, 85, 81, 90, 92, 94, 96, 97, 95, 100, 111, 104, 105, 110, 120,
             150,
             160]
    TEMP = [75, 80, 90, 100, 76, 90, 100, 110, 115, 130, 77, 83]

    def __init__(self, file_path):
        self.file_path = file_path

    async def start(self):
        data = await asyncio.to_thread(Functions.read_jsonfile, self.file_path)
        client = IoTHubDeviceClient.create_from_connection_string(self.CONN_STRING)

        await asyncio.to_thread(client.connect)

        for value in data.values():
            for v in value:
                Latitude = v[0]
                Longitude = v[1]
                now = datetime.now()
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                curr_temp = random.choice(self.TEMP)
                curr_speed = random.choice(self.SPEED)
                curr_tire_pressure = random.choice(self.TIRE_PRESURE)
                curr_alert = random.choice(self.ALERT)
                message_content = {
                    'DeviceId': 'jason',
                    'Latitude': Latitude,
                    'Longitude': Longitude,
                    'time': current_time,
                    'temp': curr_temp,
                    'tire_press': curr_tire_pressure,
                    'speed': curr_speed,
                    'alert': curr_alert
                }

                message = Message(json.dumps(message_content))
                await asyncio.to_thread(client.send_message, message)
                print("Message sent to Azure IoT Hub:", message_content)
                await asyncio.sleep(30)


async def main():
    car = FirstCar('routes/sofia-burgas-route.json')
    await car.start()


if __name__ == "__main__":
    asyncio.run(main())
