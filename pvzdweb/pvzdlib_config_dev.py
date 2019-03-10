""" create an invocation class specific for AODSFileHandler """
import collections
from pathlib import Path
from PVZDpy.config.policystore_backend_abstract import PolicyStoreBackendAbstract

class PolicyStoreBackendDB():
     pass

class PVZDlibConfigDatabase():

     # Store policy artifacts in database
     polstore_backend = PolicyStoreBackendDB()

     # Trusted Fedop Certificates: Always stored in filesystem
     trustedcerts = Path('/Users/admin/devl/python/identinetics/PVZDlib/PVZDpy/config')

     debug = False
     noxmlsign = False  # developmet: skip interactive signing

