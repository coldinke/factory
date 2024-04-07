import json
import logging
import paho.mqtt.client as mqtt
from models import SensorData
from db import save_sensor_data
from utils import setup_logging
from config import settings

All_sensor_data = list()
setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 

def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Connected to MQTT Broker with result code {reason_code}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global sensor_data
    payload = msg.payload.decode()
    logger.info(f"Received sensor data: {payload}")
    try:
        data = json.loads(payload)
        sensor_data_list = list()
        for node_id, node_data in data.items():
            sensor_data= SensorData(
                nodeno=int(node_data["nodeno"]),
                temperature=node_data["temp"],
                humidity=node_data["humi"]
            )
            sensor_data_list.append(sensor_data.dict())
        all_sensor_data.extend(sensor_data_list)
        save_sensor_data(sensor_data_list)
    except (ValueError, KeyError) as e:
        logger.error(f"Error parsing sensor data: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message


def setting_mqtt_conf(user, passwd):
    logger.info(f"Setting MQTT connection's arguments: {user}:{passwd}")
    client.username_pw_set(username=user, password=passwd)


def connect_to_mqtt(host, port, keepalive):
    try:
        client.connect(host, port, keepalive)
        logger.info(f"Connceted to MQTT Broker at {host}:{port}")
    except Exception as e:
        logger.error(f"Error connecting to MQTT Broker: {e}, so EXIT with 1")
        exit(1)

def start_mqtt_client():
    try:
        client.loop_start()
        logger.info("MQTT client started")
    except Exception as e:
        logger.error(f"Error starting MQTT client: {e}")

    
def stop_mqtt_client():
    try:
        client.loop_stop()
        logger.info("MQTT client stopped")
    except Exception as e:
        logger.error(f"Error stopping MQTT client: {e}")