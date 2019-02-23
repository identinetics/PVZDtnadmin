import logging
import logging.config
import os
from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.aodsfilehandler import AODSFileHandler
from PVZDpy.constants import LOGLEVELS
from invocation.clipmp import CliPmp
import loggingconfig


def run_me():
    if sys.version_info < (3, 6):
        raise "must use python 3.6 or greater"

    logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
    if 'LOGLEVEL' in os.environ and os.path.isfile(os.environ['LOGLEVEL']):
        loglevel = os.environ['LOGLEVEL']
    else:
        loglevel = 'INFO'
    logging_config = loggingconfig.LoggingConfig(logbasename,
                                                 console=True,
                                                 file_level=loglevel)
    exception_lvl = LOGLEVELS['ERROR']
    logging.debug('logging level=' + loglevel)

    invocation = CliPmp()
    aodsListHandler = AodsListHandler(AODSFileHandler())
    aodsListHandler.aods_append()


if __name__ == '__main__':
    run_me()
