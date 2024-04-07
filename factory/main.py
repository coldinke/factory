import uvicorn
import logging
import json
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from mqtt_client import setting_mqtt_conf, connect_to_mqtt, start_mqtt_client, stop_mqtt_client, all_sensor_data 
from utils import setup_logging
from config import settings

sensor_data = None

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        if all_sensor_data:
            data = all_sensor_data.copy()
            all_sensor_data.clear()
            await websocket.send_text(json.dumps(data))

@app.get("/sensor_data")
def get_sensor_data():
    return sensor_data

@app.get("/", response_class=HTMLResponse)
async def render_html(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"request": request, "sensor_data": sensor_data})


def main():
    logger.info(f"The MQTT connection argument: {settings.mqtt_host}:{settings.mqtt_port} Keep-alive: {settings.mqtt_keepalive}")
    logger.info(f"The Webserver start at {settings.app_host}:{settings.app_port}")
    
    # 设置 MQTT 的连接参数
    setting_mqtt_conf(settings.mqtt_user, settings.mqtt_passwd)
    # 连接到MQTT Broker
    connect_to_mqtt(settings.mqtt_host, settings.mqtt_port, settings.mqtt_keepalive)
    # 启动MQTT客户端
    start_mqtt_client()
    # 启动FastAPI应用程序
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
    # 停止MQTT客户端
    stop_mqtt_client()


if __name__ == '__main__':
    main()