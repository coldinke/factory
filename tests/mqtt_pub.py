import time
import json
import paho.mqtt.client as client
import paho.mqtt.publish as publish



# MQTT回调函数
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        # userdata.pop()
        print("sent done...")
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
        print("This is due to an unavoidable race-condition:")
        print("* publish() return the mid of the message sent.")
        print("* mid from publish() is added to unacked_publish by the main thread")
        print("* on_publish() is called by the loop_start thread")
        print("While unlikely (because on_publish() will be called after a network round-trip),")
        print(" this is a race-condition that COULD happen")
        print("")
        print("The best solution to avoid race-condition is using the msg_info from publish()")
        print("We could also try using a list of acknowledged mid rather than removing from pending list,")
        print("but remember that mid could be re-used !")

# unacked_publish = set()

sensor_data = [
    {"nodeno": "1", "temp": 10.1, "humi": 10.1},
    {"nodeno": "2", "temp": 11.1, "humi": 12.1},
    {"nodeno": "3", "temp": 12.1, "humi": 13.1},
    {"nodeno": "4", "temp": 13.1, "humi": 14.1},
    {"nodeno": "5", "temp": 14.1, "humi": 14.1},
    {"nodeno": "6", "temp": 15.1, "humi": 15.1},
    {"nodeno": "7", "temp": 16.1, "humi": 16.1},
    {"nodeno": "8", "temp": 17.1, "humi": 17.1},
]

json_data = dict()

for i, data in enumerate(sensor_data, start=1):
    json_data[f"no{i}"] = data

json_str = json.dumps(json_data)
print(json_str)

mqttc = client.Client(client.CallbackAPIVersion.VERSION2)
# mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

mqttc.user_data_set(json_str)
mqttc.username_pw_set("user01", "1234")
mqttc.connect("192.168.25.80", 1883, 60)
mqttc.loop_start()

# Our application produce some messages
msg_info = mqttc.publish("test/mqtt", json_str, qos=1)

# Due to race-condition described above, the following way to wait for all publish is safer
msg_info.wait_for_publish()

mqttc.disconnect()
mqttc.loop_stop()

# publish.single("test/mqtt", json_str, hostname="192.168.25.80")