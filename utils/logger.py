import logging

def get_logger(name):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s - %(funcName)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    return logger

logger = get_logger('fastapi_logger')