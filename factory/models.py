from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    nodeno: int
    temperature: float
    humidity: float
    timestamp: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = datetime.now()