import logging
import logging.config


LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
# LOGGING_LEVEL = 'logging.DEBUG'
LOGGING_LOCATION = 'onelove/logs'

# create logger
log = logging.getLogger('onelove')

log.setLevel(level=logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)

# create formatter
formatter = logging.Formatter(LOGGING_FORMAT)

# add formatter to ch
ch.setFormatter(formatter)

# add ch to log
log.addHandler(ch)