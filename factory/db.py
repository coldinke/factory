import logging
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import SensorData
from utils import setup_logging
from config import settings

# Initalizetion
setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 
engine = create_engine(settings.db_path, echo=True)
Base = declarative_base()

class SensorDataDB(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    nodeno = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime)

    def __repr__(self):
        return f"SensorData(nodeno={self.nodeno}, temperature={self.temperature}, humidity={self.humidity}, timestamp={self.timestamp})"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def save_sensor_data(sensor_data):
    session = Session()
    try:
        for data in sensor_data:
            sensor_model = SensorData.parse_obj(data)
            db_data = SensorDataDB(nodeno=sensor_model.nodeno,
                                   temperature=sensor_model.temperature,
                                   humidity=sensor_model.humidity,
                                   timestamp=sensor_model.timestamp)
            logger.info(f"Sensor data: {db_data}")
            session.add(db_data)
        session.commit()
        logger.info("Sensor data saved to database")
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving sensor data: {e}")
        raise
    finally:
        session.close()
    