import sys

import logging


class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


log_format = '%(asctime)s - %(name)s - {%(threadName)s} [%(levelname)s] : %(message)s'
h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.DEBUG)
h1.addFilter(InfoFilter())
h1.setFormatter(logging.Formatter(log_format))
h2 = logging.StreamHandler()
h2.setLevel(logging.WARNING)
h2.setFormatter(logging.Formatter(log_format))


if __name__ == '__main__':
    logger = logging.getLogger("__name__")
    logger.setLevel(logging.INFO)
    logger.addHandler(h1)
    logger.addHandler(h2)

    logger.error('error')
    logger.warning('warning')
    logger.info('info')
    logger.debug('debug')
