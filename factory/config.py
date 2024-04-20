from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # APP configuration
    app_name: str = "Factory"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    log_path: str = "./logs/factory.log"
    db_path: str = "sqlite:///data/sensors.db"
    # MQTT connection arguments
    mqtt_host: str = "ubuntu1.orb.local"
    mqtt_port: int = 1883  
    mqtt_keepalive: int = 60
    mqtt_user: str = "user01"
    mqtt_passwd: str = "1234"
    mqtt_sub_topic: str = "/test/hello_pub"
    mqtt_pub_topic: str = "/test/hello"

    
settings = Settings()