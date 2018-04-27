# Generated by Django 2.0.3 on 2018-04-27 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0011_auto_20180417_2138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gvfederation',
            options={'verbose_name': 'Federation', 'verbose_name_plural': 'Federation'},
        ),
        migrations.AlterModelOptions(
            name='gvfederationorg',
            options={'ordering': ('gvOuId',), 'verbose_name': 'Federation Member', 'verbose_name_plural': 'Federation Members'},
        ),
        migrations.AlterModelOptions(
            name='gvorganisation',
            options={'ordering': ['o'], 'verbose_name': 'Organisation', 'verbose_name_plural': 'Organisationen'},
        ),
        migrations.AlterModelOptions(
            name='gvorgunit',
            options={'ordering': ['gvOuVKZ'], 'verbose_name': 'Organisationseinheit', 'verbose_name_plural': 'Organisationseinheiten'},
        ),
        migrations.AlterModelOptions(
            name='gvuserportal',
            options={'ordering': ('cn',), 'verbose_name': 'Stammportal', 'verbose_name_plural': 'Stammportale'},
        ),
        migrations.AddField(
            model_name='gvfederationorg',
            name='gvOuId3',
            field=models.ForeignKey(blank=True, help_text='gvOuId des Dienstleister', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Dienstleister', to='tnadmin.GvOrganisation', verbose_name='Dienstleister'),
        ),
        migrations.AlterField(
            model_name='gvfederation',
            name='gvFederationName',
            field=models.CharField(help_text='Eindeutige Bezeichnung der Federation im E-Mail-Adressen Format nach RFC 822 beziehungsweise als DNS Name. Das Zeichen SLASH darf nicht verwendet werden. Für den Portalverbund der österreichischen Behörden gem. Portalverbundvereinbarungist als gvFederationName der Wert portalverbund.gv.at festgelegt.Organisationsinterne Federations SOLLEN mit "internal@" + Domain-Name der Organisation. (z.B. intern@lfrz.at) bezeichnet werden.', max_length=64, unique=True, verbose_name='Federation Name'),
        ),

    ]
