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
        return result
    finally:
        session.close()
        

def get_all_sensors() -> list[SensorData]:
    session = Session()
    all_sensor_data = list()
    try:
        for i in range(9):
            sensor_data_db = session.query(SensorDataDB)\
                .filter(SensorDataDB.nodeno == i)\
                .order_by(SensorDataDB.timestamp.desc()).first()
            if sensor_data_db:
                sensor_data = SensorData(
                    nodeno=sensor_data_db.nodeno,
                    temperature=sensor_data_db.temperature,
                    humidity=sensor_data_db.humidity,
                    timestamp=sensor_data_db.timestamp,
                )
                all_sensor_data.append(sensor_data)
        return all_sensor_data
    finally:
        session.close()

def get_sensor_data_history(nodeno): 
    session = Session()
    res = list()
    try: 
        result = session.query(SensorDataDB)\
           .filter(SensorDataDB.nodeno == nodeno)\
           .order_by(SensorDataDB.timestamp.desc())\
           .limit(10)\
           .all()
        print(result)
        return result
    finally:
        session.close() 
