import sys
from pathlib import Path
from PVZDpy.config.appconfig_abstract import PVZDlibConfigAbstract
from common.policystore_backend_django import PolicyStoreBackendDjango


class PVZDlibConfig(PVZDlibConfigAbstract):
    """ Python configuration object for PVZDlib/PVZDpy """
    def _set_config(self):
        config = self.config['confkey']
        # Store policy artifacts in file system relative to this config
        config.polstore_backend = PolicyStoreBackendDjango()

        # Trusted Fedop Certificates: Always stored in filesystem
        config.trustedcertsdir = Path(__file__).parent / 'tests' / 'trustedcerts'

        config.xmlsign = False  # False: only for development to skip interactive signing
        config.debug = False
        config.projhome = Path('sys.argv[0]').parent.parent
