from pydantic import BaseModel 
from sqlalchemy import  Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

class SensorData(BaseModel):
    nodeno: int
    temperature: float
    timestamp: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = datetime.now()

class ControlData(BaseModel):
    state: int
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
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"SensorData(nodeno={self.nodeno}, \
            temperature={self.temperature}, \
                timestamp={self.timestamp})"

class ControlDataDB(Base):
    __tablename__ = 'control_data'

    id = Column(Integer, primary_key=True)
    state = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"CO1Data(state={self.state}, timestamp={self.timestamp})"

