import json
from django.conf import settings


def getPolicyDict_from_json() -> dict:
    with open(settings.PVZD_SETTINGS['policydir']) as fd:
        return json.load(fd)
