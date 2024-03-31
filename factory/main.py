import logging

# The MQTT connection arguments
MQTT_HOST = "192.168.1.110"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60


def setup_logging(log_file="./logs/example.log", log_file_mode="w",log_level=logging.INFO):
    """ Set default logging config """
    logging.basicConfig(filename=log_file, filemode=log_file_mode,level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')




def main():
    setup_logging('./logs/factory.log')

    logger = logging.getLogger(__name__)

    logger.info(f"The MQTT connection argument: {MQTT_HOST}:{MQTT_PORT} Keep-alive: {MQTT_KEEPALIVE}")
    logger.warning("THIS IS A WARNING MESSAGE")



if __name__ == '__main__':
    main()