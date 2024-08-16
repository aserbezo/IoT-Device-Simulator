from dotenv import load_dotenv
import os
import json
import time
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from datetime import datetime
import random

#######################################################################
# Set a seed for random number generation to ensure reproducibility
#######################################################################
random.seed(50)

########################################################################
# Load environment variables from .env file
########################################################################
load_dotenv()

########################################################################
# Retrieve connection strings from environment variables
########################################################################
jasonstatham_connection_string = os.getenv('jasonstatham_connection_string')
jamesbond_connection_string = os.getenv('jamesbond_connection_string')
johnyenglish_connection_string = os.getenv('johnyenglish_connection_string')

########################################################################
# Load the JSON route data from files
########################################################################
with open('routes/sofia-burgas-route.json', 'rb') as file, open('routes/sofia-varna-route.json', 'rb') as file1, open(
        'routes/sofia-vidin-route.json', 'rb') as file2:
    # Load the JSON data from the file
    jasonroute = file.read().decode('utf-8')
    jamesroute = file1.read().decode('utf-8')
    johnyroute = file2.read().decode('utf-8')

########################################################################
# Parse the JSON data into Python dictionaries
########################################################################
sofia_burgas = json.loads(jasonroute)
sofia_varna = json.loads(jamesroute)
sofia_vidin = json.loads(johnyroute)

########################################################################
# Define possible values for speed, temperature, alerts, and tire pressure
########################################################################
speed = [60, 64, 65, 68, 70, 75, 77, 74, 80, 82, 88, 85, 81, 90, 92, 94, 96, 97, 95, 100, 111, 104, 105, 110, 120, 150,160]
temp = [75, 80, 90, 100, 76, 90, 100, 110, 115, 130, 77, 83]
tire_pressure = [30, 31, 32, 33, 29, 25]
acceleration = [2.5,3.2,-1.8,0.0,4.1,-2.3,1.7,2.9,3.5,-0.7]
rpm = [2200, 2400, 2100, 2300, 2500, 2600, 2400, 2000, 2200, 2350]
braking = [-2.5, -3.0, -1.8, -4.2, -2.9, -3.3, -1.5, -2.7, -4.0, -2.1]
seatbelt_status_array = [True, True, False, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False]
engine_check = [True, True, False, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False]
low_fuel = [True, True, False, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False]
tire_pressure_low = [True, True, False, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False]
battery_low = [True, True, False, False, True, False, True, True, False, False, False, True, False, True, False, False, False, False, False, False, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, True, False, False, False, False, False, False, True, False, False, False, False, False, True, True, True, True, False, False, False, True, False, True, True, True, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, True, False, False, False]
voltage = [12.6, 13.2, 12.8, 13.0, 12.7, 12.9, 13.1, 12.5, 12.8, 13.3]

######################################################################
# delay to send the messages to IoT hub
######################################################################

time_delay = 10

########################################################################
# Function to send a message to the Azure IoT Hub
########################################################################
async def send_message_to_iot_hub(conn_str, message_content):
    try:
        # Create an instance of the IoT Hub device client
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        if client is None:
            raise Exception("Failed to create IoT Hub device client.")

        # Connect the client to the IoT Hub
        await client.connect()

        # Create a Message object with the message content
        message = Message(json.dumps(message_content))

        # Send the message
        await client.send_message(message)
        print("Message sent to Azure IoT Hub:", message_content)

    except Exception as e:
        print("Error:", e)

    finally:
        # Disconnect the client
        if client:
            await client.disconnect()


########################################################################
# Function to simulate Jason's car sending data to IoT Hub
########################################################################
async def jason_car():
    for value in sofia_burgas.values():
        # Extract the latitude and longitude from the route data
        for i in value:
            Latitude = i[1]
            Longitude = i[0]
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            curr_temp = random.choice(temp)
            curr_speed = random.choice(speed)
            curr_tire_pressure = random.choice(tire_pressure)
            curr_acceleration = random.choice(acceleration)
            curr_rpm = random.choice(rpm)
            curr_braking = random.choice(braking)
            seatbelt_status = random.choice(seatbelt_status_array)
            curr_engine_check = random.choice(engine_check)
            curr_low_fuel = random.choice(low_fuel)
            curr_tire_pressure_low = random.choice(tire_pressure_low)
            curr_battery_low = random.choice(battery_low)
            curr_voltage = random.choice(voltage)
            message_content = {
                "vehicle_id": "ABC12345",
                "timestamp": current_time,
                "location": {
                    "latitude": Latitude,
                    "longitude": Longitude,
                },
                "speed": curr_speed,  # speed in miles per hour
                "engine_status": {
                    "rpm": curr_rpm,
                    "temperature": curr_temp,  # temperature in celsie
                },
                "battery_status": {
                    "voltage": curr_voltage,  # battery voltage in volts
                    "charge_state": "charging"
                },
                "tire_pressure": {
                    "front_left": curr_tire_pressure,  # pressure in PSI
                    "front_right": curr_tire_pressure,
                    "rear_left": curr_tire_pressure,
                    "rear_right": curr_tire_pressure
                },
                "driver_behavior": {
                    "acceleration": curr_acceleration,
                    "braking": curr_braking,
                    "seatbelt_status": seatbelt_status

                },
                "alerts": {
                    "engine_check": curr_engine_check,
                    "low_fuel": curr_low_fuel,
                    "tire_pressure_low": curr_tire_pressure_low,
                    "battery_low": curr_battery_low
                }
            }

            # Send the message to IoT Hub asynchronously
            await send_message_to_iot_hub(jasonstatham_connection_string, message_content)
            await asyncio.sleep(time_delay)  # Adjust for faster/slower update frequency


########################################################################
# Function to simulate James's car sending data to IoT Hub
########################################################################
async def james_car():
    for value in sofia_varna.values():
        for i in value:
            Latitude = i[1]
            Longitude = i[0]
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            curr_temp = random.choice(temp)
            curr_speed = random.choice(speed)
            curr_tire_pressure = random.choice(tire_pressure)
            curr_acceleration = random.choice(acceleration)
            curr_rpm = random.choice(rpm)
            curr_braking = random.choice(braking)
            seatbelt_status = random.choice(seatbelt_status_array)
            curr_engine_check = random.choice(engine_check)
            curr_low_fuel = random.choice(low_fuel)
            curr_tire_pressure_low = random.choice(tire_pressure_low)
            curr_battery_low = random.choice(battery_low)
            curr_voltage = random.choice(voltage)
            message_content = {
                "vehicle_id": "ABC12346",
                "timestamp": current_time,
                "location": {
                    "latitude": Latitude,
                    "longitude": Longitude,
                },
                "speed": curr_speed,  # speed in miles per hour
                "engine_status": {
                    "rpm": curr_rpm,
                    "temperature": curr_temp,  # temperature in celsie
                },
                "battery_status": {
                    "voltage": curr_voltage,  # battery voltage in volts
                    "charge_state": "charging"
                },
                "tire_pressure": {
                    "front_left": curr_tire_pressure,  # pressure in PSI
                    "front_right": curr_tire_pressure,
                    "rear_left": curr_tire_pressure,
                    "rear_right": curr_tire_pressure
                },
                "driver_behavior": {
                    "acceleration": curr_acceleration,
                    "braking": curr_braking,
                    "seatbelt_status": seatbelt_status

                },
                "alerts": {
                    "engine_check": curr_engine_check,
                    "low_fuel": curr_low_fuel,
                    "tire_pressure_low": curr_tire_pressure_low,
                    "battery_low": curr_battery_low
                }
            }

            # Run send_message_to_iot_hub asynchronously
            await send_message_to_iot_hub(jamesbond_connection_string, message_content)
            await asyncio.sleep(time_delay)  # Adjust for faster/slower update frequency


########################################################################
# Function to simulate Johny's car sending data to IoT Hub
########################################################################
async def johny_car():
    for value in sofia_vidin.values():
        for i in value:
            Latitude = i[1]
            Longitude = i[0]
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            curr_temp = random.choice(temp)
            curr_speed = random.choice(speed)
            curr_tire_pressure = random.choice(tire_pressure)
            curr_acceleration = random.choice(acceleration)
            curr_rpm = random.choice(rpm)
            curr_braking = random.choice(braking)
            seatbelt_status = random.choice(seatbelt_status_array)
            curr_engine_check = random.choice(engine_check)
            curr_low_fuel = random.choice(low_fuel)
            curr_tire_pressure_low = random.choice(tire_pressure_low)
            curr_battery_low = random.choice(battery_low)
            curr_voltage = random.choice(voltage)
            message_content = {
                "vehicle_id": "ABC12347",
                "timestamp": current_time,
                "location": {
                    "latitude": Latitude,
                    "longitude": Longitude,
                },
                "speed": curr_speed,  # speed in miles per hour
                "engine_status": {
                    "rpm": curr_rpm,
                    "temperature": curr_temp,  # temperature in celsie
                },
                "battery_status": {
                    "voltage": curr_voltage,  # battery voltage in volts
                    "charge_state": "charging"
                },
                "tire_pressure": {
                    "front_left": curr_tire_pressure,  # pressure in PSI
                    "front_right": curr_tire_pressure,
                    "rear_left": curr_tire_pressure,
                    "rear_right": curr_tire_pressure
                },
                "driver_behavior": {
                    "acceleration": curr_acceleration,
                    "braking": curr_braking,
                    "seatbelt_status": seatbelt_status

                },
                "alerts": {
                    "engine_check": curr_engine_check,
                    "low_fuel": curr_low_fuel,
                    "tire_pressure_low": curr_tire_pressure_low,
                    "battery_low": curr_battery_low
                }
            }

            # Run send_message_to_iot_hub asynchronously
            await send_message_to_iot_hub(johnyenglish_connection_string, message_content)
            await asyncio.sleep(time_delay)  # Adjust for faster/slower update frequency


########################################################################
# Function to run all car simulation functions concurrently
########################################################################
async def run_all_functions():
    # Run main() and main1() concurrentl y
    results = await asyncio.gather(
        jason_car(),
        johny_car(),
        james_car()
    )

    print("Both functions completed")
    for result in results:
        print(result)


# Run the function to execute both main() and main1() concurrently
asyncio.run(run_all_functions())

"""
Key Points:
Environment Variables: Used for storing sensitive connection strings.
Random Values: Speed, temperature, tire pressure, and alerts are simulated with random values.
Async Functions: Asynchronous operations ensure that messages are sent efficiently without blocking the execution.
Concurrency: All three car simulations run concurrently, simulating real-time data transmission from multiple devices.
"""
