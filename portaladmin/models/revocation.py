from django.db import models

class Revocation:
    cert = models.CharField(
        unique=True,
        verbose_name='Zertifikat',
        help_text='X.509 cert PEM ohen Whitespace',
        max_length=128)
