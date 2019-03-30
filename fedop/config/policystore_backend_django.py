import tempfile
from pathlib import Path
from PVZDpy.config.policystore_backend_abstract import PolicyStoreBackendAbstract
from PVZDpy.userexceptions import PolicyJournalNotInitialized
from fedop.models.policystorage import PolicyStorage


class PolicyStoreBackendDjango(PolicyStoreBackendAbstract):
    def __init__(self):
        pass

    def read_or_fail_policystorage(self) -> None:
        if not hasattr(self, 'dbo'):
            try:
                self.dbo = PolicyStorage.objects.get(id=1)
            except Exception as e:
                raise PolicyJournalNotInitialized

    def read_or_init_policystorage(self) -> None:
        if hasattr(self, 'dbo'):
            self.dbo = PolicyStorage.objects.get(id=1)
        else:
            self.dbo = PolicyStorage(id=1)
            self.dbo.save()
        #dbo = PolicyStorage.objects.get(id=1)
        #if not dbo:
        #    print('bug')

    def get_policy_journal_xml(self) -> bytes:
        self.read_or_fail_policystorage()
        return bytes(self.dbo.policy_journal_xml)

    def get_policy_journal_path(self) -> Path:
        # copy policy journal from db to temp file; do not close, refresh if exists.
        if hasattr(self, 'policy_journal_xml_fd'):
            self.policy_journal_xml_fd.seek(0)
        else:
            self.policy_journal_xml_fd = tempfile.NamedTemporaryFile(mode='wb', prefix='pvzdpj_', suffix='.xml')
        self.policy_journal_xml_fd.write(self.get_policy_journal_xml())
        self.policy_journal_xml_fd.flush()
        return Path(self.policy_journal_xml_fd.name)

    def get_policy_journal_json(self) -> str:
        self.read_or_fail_policystorage()
        if not self.dbo.policy_journal_json:
            raise PolicyJournalNotInitialized
        return self.dbo.policy_journal_json

    def get_poldict_json(self) -> str:
        self.read_or_fail_policystorage()
        return self.dbo.policy_dict_json

    def get_poldict_html(self) -> str:
        self.read_or_fail_policystorage()
        return self.dbo.policy_dict_html

    def get_shibacl(self) -> bytes:
        self.read_or_fail_policystorage()
        return bytes(self.dbo.shibacl)

    def get_trustedcerts_report(self) -> str:
        self.read_or_fail_policystorage()
        return self.dbo.trustedcerts_report

    # ---

    def set_policy_journal_xml(self, xml_bytes: bytes) -> None:
        self.read_or_init_policystorage()
        self.dbo.policy_journal_xml = xml_bytes
        self.dbo.save()

    def set_policy_journal_json(self, json_str: str) -> None:
        self.read_or_init_policystorage()
        self.dbo.policy_journal_json = json_str
        self.dbo.save()

    def set_poldict_json(self, json_str: str) -> None:
        self.read_or_init_policystorage()
        self.dbo.policy_dict_json = json_str
        self.dbo.save()

    def set_poldict_html(self, html_str: str) -> None:
        self.read_or_init_policystorage()
        self.dbo.policy_dict_html = html_str
        self.dbo.save()

    def set_shibacl(self, xml_bytes: bytes) -> None:
        self.read_or_init_policystorage()
        self.dbo.shibacl = xml_bytes
        self.dbo.save()

    def set_trustedcerts_report(self, t: str) -> None:
        self.read_or_init_policystorage()
        self.dbo.trustedcerts_report = t
        self.dbo.save()

    # ---

    def reset_pjournal_and_derived(self) -> None:
        self.read_or_init_policystorage()
        self.dbo.policy_journal_xml = b''
        self.dbo.policy_journal_json = ''
        self.dbo.policy_dict_json = ''
        self.dbo.policy_dict_html = ''
        self.dbo.shibacl = b''
        self.dbo.trustedcerts_report = ''
        self.dbo.save()

    def __str__(self) -> str:
        if hasattr(self, 'dbo'):
            s = 'len(jounal_xml)= %s' % self.dbo.policy_journal_xml
            if hasattr(self, 'policy_journal_xml_fd'):
                s += str(Path(policy_journal_xml_fd.name).name)
        else:
            s = 'storage not initialized'
        return s

