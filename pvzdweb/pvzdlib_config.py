""" create an invocation class specific for AODSFileHandler """
import collections
from pathlib import Path
from PVZDpy.config import PolicyStoreBackendFile

class PVZDlibConfigDefault():
     debug = False
     noxmlsign = False  # developmet: skip interactive signing

     # Store policy artifacts in file system
     polstore_dir = Path('/config/policystore/')
     policy_store_backendfile = PolicyStoreBackendFile(polstore_dir)
     polstore_callback = policy_store_backendfile

     # Trusted Fedop Certificates: Always stored in filesystem
     trustedcerts = Path('/config/trustedcerts.json')
