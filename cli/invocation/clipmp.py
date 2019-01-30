import argparse, getpass, os, sys
from . import AbstractInvocation
from PVZDpy.constants import LOGLEVELS
from PVZDpy.userexceptions import *

__author__ = 'r2h2'

class CliPmp(AbstractInvocation):
    """ define CLI invocation for PMP. Test runner can use this by passing testargs """

    def _get_from_env(self, argname):
        # argname must be _lowercase_ (for self.args); the env var mnust be uppercase
        if not getattr(self.args, argname, False):
            env_name = 'POLMAN_%s' % argname.upper()
            if env_name in os.environ:
                setattr(self.args, argname, os.environ[env_name])
            else:
                raise InvalidArgumentValueError('neither --%s nor %s provided' % (argname, env_name))

    def __init__(self, testargs=None):
        self._parser = argparse.ArgumentParser(description='Policy Management Point V%s')
        if 'POLMAN_AODS' in os.environ and os.path.isfile(os.environ['POLMAN_AODS']):
            self._parser.add_argument('-a', '--aods', dest='aods', default=os.environ['POLMAN_AODS'],
                                      help=argparse.SUPPRESS)
        else:
            self._parser.add_argument('-a', '--aods', dest='aods',
                help='Policy journal (append only data strcuture). This value is optional if provided via POLMAN_AODS in env')
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
        if 'POLMAN_TRUSTEDCERTS' in os.environ and os.path.isfile(os.environ['POLMAN_TRUSTEDCERTS']):
            self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts',
                 default=os.environ['POLMAN_TRUSTEDCERTS'], help=argparse.SUPPRESS)
        else:
            self._parser.add_argument('-t', '--trustedcerts', dest='trustedcerts',
                 help='file containing json-array of PEM-formatted certificates trusted to sign the aods. This value is optional if provided via POLMAN_TRUSTEDCERTS in env')
        self._parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        _subparsers = self._parser.add_subparsers(dest='subcommand', help='sub-command help')

        # create the subparser for the "create" command
        self._parser_create = _subparsers.add_parser('create', help='create a new journal')

        # create the subparser for the "append" command
        self._parser_append = _subparsers.add_parser('append', help='append a record to the journal')
        self._parser_append.add_argument('input', type=argparse.FileType('r', encoding='utf8'),
             help='file containing the records to be added in JSON')

        # create the subparser for the "read" command
        self._parser_append = _subparsers.add_parser('read', help='read, verify and transform the journal')
        self._parser_append.add_argument('-P', '--poldirhtml', type=argparse.FileType('w', encoding='utf8'),
             help='output policy directory as HTML)')
        self._parser_append.add_argument('-p', '--poldirjson', type=argparse.FileType('w', encoding='utf8'),
             help='dump policy directory as JSON)')
        self._parser_append.add_argument('-j', '--journal', type=argparse.FileType('w', encoding='utf8'),
             help='output Journal as JSON)')
        self._parser_append.add_argument('--shibacl', dest='shibacl', type=argparse.FileType('w', encoding='utf8'),
             help='output admin certificates as Shibboleth SP externam AccessControl XML document')
        self._parser_append.add_argument('--printtrustedcerts', dest='printtrustedcerts', type=argparse.FileType('w', encoding='utf8'),
             help='output admin certificates as text')
        # TODO: implement range and diff listings
        #self._parser_append.add_argument('-r', '--range', choices=['all', 'from', 'new'], default='all',
        #                                 help='read all (starting with the big bang), or new (what has changes since last time)')
        #self._parser_append.add_argument('-s', '--sequence', type=int, help='output from this record onwards')

        # create the subparser for the "revokeCert" command
        self._parser_revoke = _subparsers.add_parser('revokeCert', help='revoke certificate')
        self._parser_revoke.add_argument('cert', type=argparse.FileType('r', encoding='utf8'), nargs='?', default=None,
             help='certificate to be revoked')

        # post-processing: parse, get defaults from env, validate
        if (testargs):
            self._parser_append = _subparsers.add_parser('scratch', help='scratch the AODS')
            self.args = self._parser.parse_args(testargs)
        else:
            self.args = self._parser.parse_args()  # regular case: use sys.argv

        self.args.list_trustedcerts = False  # required by aodsfilehanlder.__init__(), but only used in PEP

        if not hasattr(self.args, 'loglevel_str') or self.args.loglevel_str is None:
            self.args.loglevel_str = 'INFO'

        if self.args.subcommand == 'append':
            self.args.inputfilename = self.args.input.name
            self.args.input.close()  # why? unittest comlpains about files left open -> close here and reopen later
        if self.args.subcommand != 'create' and not self.args.aods:
            print('missing argument -a/--aods)')
            exit(1)
        if self.args.subcommand == 'read':
            if getattr(self.args, 'journal', False):
                # close file and pass it as name (handle open/close locally)
                fn = self.args.journal.name
                self.args.journal.close()
                self.args.journal = fn

        if self.args.printargs:
            for opt in [a for a in dir(self.args) if not a.startswith('_')]:
                print(opt + '=' + str(getattr(self.args, opt)))

        self._get_from_env('aods')
        self._get_from_env('trustedcerts')
