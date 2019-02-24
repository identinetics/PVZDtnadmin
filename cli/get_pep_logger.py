import logging

def get_pep_logger(loglevel: int=None) -> logging.Logger:
    """ pep logs to stdout. Storage, rotation etc. is a concern of the environment """
    ll = logging.INFO if loglevel is None else loglevel
    logger = logging.getLogger()
    logger.setLevel(ll)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s  [%(filename)s:%(lineno)s] %(message)s'))
    logger.addHandler(handler)
    return logger