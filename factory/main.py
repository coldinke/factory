import uvicorn
import logging
import asyncio
import json
from config import settings
from db import get_sensor_data_by_no, get_all_sensors, get_sensor_data_history
from fastapi import FastAPI, Request, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from mqtt_client import connect_to_mqtt, publish, subscribe, run_mqtt, get_mqtt_pub_client
from utils import setup_logging
from models import SensorData

app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://localhost:8000",
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def return_health():
    return {"message": "Pong"}

@app.get("/sensor_data/history/{nodeno}", response_model=list[SensorData])
def get_node_history(nodeno: int):
    data = get_sensor_data_history(nodeno)
    return data

@app.get("/sensor_data/{nodeno}", response_model=SensorData)
def get_sensor_data(nodeno: int):
    data = get_sensor_data_by_no(nodeno) 
    logger.info(f"nodeNo: {nodeno}, data: {data}")
    return data

@app.get("/all_sensor_data", response_model=list[SensorData])
def get_all_sensor_data():
    all_sensor_data = get_all_sensors()
    return all_sensor_data

@app.get("/control/node")
def control_node_endpoint(node_id: int, on_off: str):
    message = {"nodeNo": node_id, "status": on_off}
    message_json = json.dumps(message)
    mqtt_pub_client = get_mqtt_pub_client(settings.mqtt_user, settings.mqtt_passwd, settings.mqtt_host, settings.app_port, settings.mqtt_keepalive)
    publish(mqtt_pub_client, settings.mqtt_pub_topic, message_json)
    return message 

# @app.get("/", response_class=HTMLResponse)
# async def render_html(request: Request):
#     return templates.TemplateResponse(
#         request=request,
#         name="index.html", 
#         context={"request": request, "sensor_data": sensor_data})

async def mqtt_subscribe(mqtt_client):
    await subscribe(mqtt_client, settings.mqtt_sub_topic)
    mqtt_client.loop_start()

@app.on_event("startup")
async def startup_event():
    mqtt_sub_client = connect_to_mqtt(settings.mqtt_user, settings.mqtt_passwd, settings.mqtt_host, settings.mqtt_port, settings.mqtt_keepalive)
    asyncio.create_task(mqtt_subscribe(mqtt_sub_client))

@app.on_event("shutdown")
async def shutdown_event():
    mqtt_sub_client.loop_stop()

def main():
    logger.info(f"The MQTT connection argument: {settings.mqtt_host}:{settings.mqtt_port} Keep-alive: {settings.mqtt_keepalive}")
    logger.info(f"The Webserver start at {settings.app_host}:{settings.app_port}")
    
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)



if __name__ == '__main__':
    main()