from django.contrib import admin

from ..models import MDstatementHistory


class ReadOnlyAdmin(admin.ModelAdmin):  # TODO move to util
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MDstatementHistory)
class MDstatement_historyAdmin(ReadOnlyAdmin):
    actions = None
    list_display = ['entityID', 'status']
    readonly_fields = list_display
    search_fields = ('entityID', 'status', )




