import django.dispatch

md_statement_edit_starts = django.dispatch.Signal(providing_args=["md_statement_id"])
