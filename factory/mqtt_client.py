import json
import logging
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
from models import SensorData, ControlData
from db import save_sensor_data, save_control_data
from utils import setup_logging
from config import settings

setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 

# connect the mqtt broker, return the client for mqtt_client
def connect_to_mqtt(user, passwd, host, port, keepalive, times=10):
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info(f"Connected to MQTT Broker with result code {reason_code}")
        else:
            logger.warning(f"Failed to connect, return code %d\n", reason_code)
        
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=user, password=passwd)
    client.on_connect = on_connect
    client.enable_logger()
    try:
        client.connect(host, port, keepalive)
        logger.info(f"Connceted to MQTT Broker at {host}:{port}")
    except Exception as e:
        times -= 1
        logger.warning(f"Error connecting to MQTT Broker: {e}, Reconnected {10 - times} times.")
        if (times == 0):
            logger.error(f"Error connecting to MQTT Broker: {e}, exit with 1.")
            exit(1)

    return client

# publish the msg to topic
def publish(client, topic, message):
    result = client.publish(topic, message)
    while True:
        if result[0] == 0:
            logger.info(f"Send {message} message successed!")
            break;
        else:
            logger.warning(f'Failed to send message!')
        
# subscribe the topic and recive the msg from topic
async def subscribe(client, topic):
    def on_message(client, userdata, msg):
        # logger = logging.getLogger(__name__)
        payload = msg.payload.decode()
        logger.info(f"Received sensor data: {payload}")
        try:
            sensor_data = payload
            data = json.loads(payload)
            sensor_data_list = list()
            for node_id, node_data in data.items():
                if node_id == "co1":
                    control_data = ControlData(state=int(node_data["state"]))
                else:
                    sensor_data= SensorData(
                        nodeno=int(node_data["nodeno"]),
                        temperature=node_data["temp"],
                        humidity=node_data["humi"]
                    )
                    sensor_data_list.append(sensor_data.dict())
            print(1)
            save_sensor_data(sensor_data_list)
            print(2)
            save_control_data(control_data) 
        except (ValueError, KeyError) as e:
            logger.error(f"Error parsing sensor data: {e}")

    client.subscribe(topic)
    client.on_message = on_message

def get_mqtt_pub_client(user, passwd, host, port, keepalive):
    mqtt_pub_client = connect_to_mqtt(user, passwd, host, port, keepalive)    
    return mqtt_pub_client

# run the client.
def run_mqtt(client: mqtt_client, topic, operation_func):
    logger.info('MQTT client started')
    client.loop_start()
    operation_func(client, topic)
    client.loop_stop()
    logger.info('MQTT client stopped')