import json
from django.http import HttpResponse
from django.template import loader
from fedop.poljournal_updater import PolicyJournalUpdater


changelist = [
    'add organization, AT:L4: 000000',
    'add organization, AT: L6',
    'add organization, AT: VKZ:UFB - 262918w',
    'add issuer, PVZD - Test - CA, IDP',
]


def pjupdate(request, mode):
    def preview(request):
        template = loader.get_template('fedop/preview.html')
        context = {'changelist': changelist}
        return HttpResponse(template.render(context, request))

    def confirm(request):
        template = loader.get_template('fedop/confirm.html')
        context = {}
        return HttpResponse(template.render(context, request))

    policy_journal_updater = PolicyJournalUpdater()
    policy_change_list = policy_journal_updater.get_changelist()
    if mode == 'preview':
        return preview(request)
    elif mode == 'confirm':
        policy_journal_updater.append_poljournal()
        if policy_journal_updater:
            return confirm(request)
        else:
            raise Http404("Must call preview before confirm")