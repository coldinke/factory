import uvicorn
import logging
import json
from config import settings
from db import get_sensor_data_by_no
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from mqtt_client import connect_to_mqtt, publish, subscribe, run_mqtt, get_mqtt_pub_client,all_sensor_data 
from utils import setup_logging
from models import SensorData

sensor_data = None

app = FastAPI()
setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if all_sensor_data is None:
            data = all_sensor_data.copy()
            all_sensor_data.clear()
            await websocket.send_text(json.dumps(data))

@app.get('/heathz')
def return_health():
    return '200'

@app.get("/sensor_data/{nodeno}", response_model=SensorData)
def get_sensor_data(nodeno: int):
    data = get_sensor_data_by_no(nodeno) 
    print(data)
    return data

@app.get("/all_sensor_data", response_model=list[SensorData])
def get_all_sensor_data():
    return all_sensor_data

@app.get("/control/node")
def control_node_endpoint(node_id: int, on_off: str):
    message = {"nodeNo": node_id, "status": on_off}
    mqtt_pub_client = get_mqtt_pub_client(settings.mqtt_user, settings.mqtt_passwd, settings.mqtt_host, settings.app_port, settings.mqtt_keepalive)
    publish(mqtt_pub_client, settings.mqtt_pub_topic, message)

# @app.get("/", response_class=HTMLResponse)
# async def render_html(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html", 
#         context={"request": request, "sensor_data": sensor_data})


def main():
    logger.info(f"The MQTT connection argument: {settings.mqtt_host}:{settings.mqtt_port} Keep-alive: {settings.mqtt_keepalive}")
    logger.info(f"The Webserver start at {settings.app_host}:{settings.app_port}")
    
    # 新建两个 mqtt 客户端，一个用于从 topic 接受消息，一个用于向 topic 推送消息 
    mqtt_sub_client = connect_to_mqtt(settings.mqtt_user, settings.mqtt_passwd, settings.mqtt_host, settings.mqtt_port, settings.mqtt_keepalive)
    
    # run the sub client
    run_mqtt(mqtt_sub_client, settings.mqtt_sub_topic, subscribe)

    uvicorn.run(app, host=settings.app_host, port=settings.app_port)



if __name__ == '__main__':
    main()