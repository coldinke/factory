from pydantic import BaseModel 
from sqlalchemy import  Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class SensorData(BaseModel):
    nodeno: int
    temperature: float
    humidity: float
    timestamp: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = datetime.now()

############################ The below is belong to the database's data model ###########################
# The database's table
Base = declarative_base()
class SensorDataDB(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    nodeno = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"SensorData(nodeno={self.nodeno}, \
            temperature={self.temperature}, \
                humidity={self.humidity}, \
                    timestamp={self.timestamp})"


