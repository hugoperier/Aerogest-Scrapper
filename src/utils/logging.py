import logging

def getLogger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]:  %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger