import argparse
import getpass
import os
import sys
from PVZDpy.userexceptions import *


class CliPmp():
    def __init__(self):
        self._parser = argparse.ArgumentParser(description='Policy Management Point V%s')
        self._parser.add_argument('-d', '--debug', dest='debug', action="store_true",
             help='trace hash chain computation')
        self._parser.add_argument('-n', '--noxmlsign', action="store_true",
             help='do not sign policy journal with xml signature')
        self._parser.add_argument('-L', '--loglevel', dest='loglevel_str', choices=LOGLEVELS.keys(),
             help='Level for file logging')
        self._parser.add_argument('-p', '--print-args', dest='printargs', action="store_true",
             help='print invocation arguments')
        self._parser.add_argument('-r', '--registrant', dest='registrant', default='',
             help='Person adding the input record (current user)')
        self._parser.add_argument('-s', '--submitter', dest='submitter', default=getpass.getuser(),
             help='Person that submitted the input record')
        self.args = self._parser.parse_args()