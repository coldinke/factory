import logging

def setup_logging(log_file="./logs/example.log", log_file_mode="w",log_level=logging.DEBUG):
    """ Set default logging config """
    logging.basicConfig(filename=log_file, filemode=log_file_mode,level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')
            