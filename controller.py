from azure.iot.device import IoTHubDeviceClient, Message
import json
import time

# Connect to PLC
plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)

# Azure IoT Device Connection String (correct one)
conn_str = "HostName=arcreate.azure-devices.net;DeviceId=f2124164-ab35-4412-aeb6-970c0c1fed9b;SharedAccessKey=3hllRw5UGyqTZnpnnyRcG0JX6vjgATO2ZQrTjfWwDdY="
client = IoTHubDeviceClient.create_from_connection_string(conn_str)

while True:
    try:
        payload = {
            "deviceId": "f2124164-ab35-4412-aeb6-970c0c1fed9b"
        }

        # Read bytes for M0 to M3
        data_m0 = plc.mb_read(0, 1)  # M0.0 to M0.7
        data_m1 = plc.mb_read(1, 1)  # M1.0 to M1.7
        data_m2 = plc.mb_read(2, 1)  # M2.0 to M2.7
        data_m3 = plc.mb_read(3, 1)  # M3.0 to M3.7

        # case1 to case7 → M0.0 to M0.6
        for i in range(7):
            payload[f"case{i+1}"] = snap7.util.get_bool(data_m0, 0, i)

        # case8 to case14 → M1.0 to M1.6
        for i in range(7):
            payload[f"case{i+8}"] = snap7.util.get_bool(data_m1, 0, i)

        # case15 → M2.0
        payload["case15"] = snap7.util.get_bool(data_m2, 0, 0)

        # pump1 → M3.0
        payload["pump1"] = snap7.util.get_bool(data_m3, 0, 0)

        # pump2 → M3.1
        payload["pump2"] = snap7.util.get_bool(data_m3, 0, 1)

        msg = Message(json.dumps(payload))
        client.send_message(msg)
        print(f"Sent to Azure IoT Hub: {payload}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(5)
