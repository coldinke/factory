import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import Base, SensorData, SensorDataDB
from utils import setup_logging
from config import settings

# Initialization 
setup_logging(settings.log_path)
logger = logging.getLogger(__name__) 
engine = create_engine(settings.db_path, echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

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
            logger.error(f"Error saving sensor data: {e}")
            raise
    finally:
        session.close()

def get_sensor_data_by_no(nodeno: int):
    session = Session()
    try:
        result = session.query(SensorDataDB)\
            .filter(SensorDataDB.nodeno == nodeno)\
            .order_by(SensorDataDB.timestamp.desc()).first()
        print(result) 
        return result
    finally:
        session.close()
        