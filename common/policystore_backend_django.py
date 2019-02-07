from pathlib import Path
from PVZDpy.config.policystore_backend_abstract import PolicyStoreBackendAbstract
from PVZDpy.userexceptions import PolicyJournalNotInitialized
from fedop.models import PolicyStorage



class PolicyStoreBackendFile(PolicyStoreBackendAbstract):
    def __init__(self, polstore_dir: Path):
        self.dbo = PolicyStorage.objects.get(id=1)

    # ---

    def get_policy_journal(self) -> bytes:
        return self.dbo.policy_journal_xml

    def get_policy_journal_path(self) -> Path:
        raise NotImplementedError()

    def get_policy_journal_json(self) -> str:
        return self.dbo.policy_journal_json

    def get_poldict_json(self) -> str:
        return self.dbo.poldict_json

    def get_poldict_html(self) -> str:
        return self.dbo.poldict_html

    def get_shibacl(self) -> bytes:
        return self.dbo.shibacl

    def get_trustedcerts_report(self) -> str:
        return self.dbo._trustedcerts_report

    # ---

    def set_policy_journal_xml(self, xml_bytes: str):
        self.dbo.policy_journal_xml = xml_bytes
        self.save()

    def set_policy_journal_json(self, json_str: str):
        self.dbo.policy_journal_json = json_str
        self.save()

    def set_policy_dict_json(self, json_str: str):
        self.dbo.policy_dict_json = json_str
        self.save()

    def set_poldict_html(self, html_str: str):
        self.dbo.policy_dict_html = html_str
        self.save()

    def set_shibacl(self, xml_bytes: str):
        self.dbo.shibacl = xml_bytes
        self.save()

    def set_trustedcerts_report(self, t: str):
        self.dbo.trustedcerts_report = t
        self.save()

    # ---

    def reset_pjournal_and_derived(self):
        self.dbo.policy_journal_xml = b''
        self.dbo.policy_journal_json = ''
        self.dbo.policy_dict_json = ''
        self.dbo.policy_dict_html = ''
        self.dbo.shibacl = b''
        self.dbo.trustedcerts_report = ''
        self.save()
