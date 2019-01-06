from django.db import models

class LdapSyncJobPull(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    add_upd_ldap_records_read = models.IntegerField(default=0)
    add_upd_records_skipped = models.IntegerField(default=0)
    add_upd_records_added = models.IntegerField(default=0)
    add_upd_records_updated = models.IntegerField(default=0)
    add_upd_records_update_failed = models.IntegerField(default=0)
    del_db_records_read = models.IntegerField(default=0)
    del_records_deleted = models.IntegerField(default=0)
    del_records_delete_failed = models.IntegerField(default=0)


class LdapSyncErrorPull(models.Model):
    ldap_dn = models.CharField(max_length=222)
    op = models.CharField(max_length=6)
    message = models.CharField(max_length=5000)
    job_id = models.ForeignKey('LdapSyncJobPull', on_delete=models.CASCADE)


class LdapSyncJobPush(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    add_upd_db_records_read = models.IntegerField(default=0)
    add_upd_records_skipped = models.IntegerField(default=0)
    add_upd_records_added = models.IntegerField(default=0)
    add_upd_records_updated = models.IntegerField(default=0)
    add_upd_records_update_failed = models.IntegerField(default=0)
    del_ldap_records_read = models.IntegerField(default=0)
    del_records_deleted = models.IntegerField(default=0)
    del_records_delete_failed = models.IntegerField(default=0)


class LdapSyncErrorPush(models.Model):
    ldap_dn = models.CharField(max_length=222)
    op = models.CharField(max_length=6)
    message = models.CharField(max_length=5000)
    job_id = models.ForeignKey('LdapSyncJobPush', on_delete=models.CASCADE)

