import json
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
import  asyncio

class Functions():
    @staticmethod
    def read_jsonfile(file_path):
        with open(file_path, 'rb') as file:
            data = file.read().decode('utf-8')
        route = json.loads(data)
        return route

    @staticmethod
    async def send_message_to_iot_hub(conn_str, message_content):
        try:
            # Create an instance of the IoT Hub device client
            client = IoTHubDeviceClient.create_from_connection_string(conn_str)

            if client is None:
                raise Exception("Failed to create IoT Hub device client.")

            # Connect the client to the IoT Hub
            await asyncio.to_thread(client.connect)

            # Create a Message object with the message content
            message = Message(json.dumps(message_content))

            # Send the message
            await asyncio.to_thread(client.send_message, message)
            print("Message sent to Azure IoT Hub:", message_content)

        except Exception as e:
            print("Error:", e)

        finally:
            # Disconnect the client
            if client:
                await asyncio.to_thread(client.disconnect)
