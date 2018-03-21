# Generated by Django 2.0.3 on 2018-03-21 20:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GvFederation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gvStatus', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], db_column='gvStatus', default='active', max_length=8, null=True, verbose_name='Status')),
                ('gvSource', models.CharField(blank=True, db_column='gvSource', default='', max_length=10, null=True, verbose_name='Änderung am/durch')),
                ('gvScope', models.CharField(db_column='gvScope', default='gv.at', max_length=32, null=True)),
                ('gvFederationName', models.CharField(help_text='Eindeutige Bezeichnung einer Federation im E-Mail-Adressen Format nach RFC 822 beziehungsweise als DNS Name. Das Zeichen SLASH darf nicht verwendet werden. Für den Portalverbund der österreichischen Behörden gem. Portalverbundvereinbarungist als gvFederationName der Wert portalverbund.gv.at festgelegt.Organisationsinterne Federations SOLLEN mit "internal@" + Domain-Name der Organisation. (z.B. intern@lfrz.at) bezeichnet werden.', max_length=64, unique=True, verbose_name='Federation Name')),
                ('gvMetaDataURL', models.URLField(help_text='Bezugspunkt für Metadaten dieser Federation (URL für signiertes SAML Metadata Aggregat)', unique=True, verbose_name='Metadata URL')),
            ],
            options={
                'verbose_name': 'Federation',
                'verbose_name_plural': 'Federations',
            },
        ),
        migrations.CreateModel(
            name='GvOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gvStatus', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], db_column='gvStatus', default='active', max_length=8, null=True, verbose_name='Status')),
                ('gvSource', models.CharField(blank=True, db_column='gvSource', default='', max_length=10, null=True, verbose_name='Änderung am/durch')),
                ('gvScope', models.CharField(db_column='gvScope', default='gv.at', max_length=32, null=True)),
                ('gvOuID', models.CharField(db_column='gvOuID', max_length=32, unique=True, verbose_name='Verwaltungskennzeichen (AT:VKZ)')),
                ('gvOuVKZ', models.CharField(db_column='gvOuVKZ', help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium) \u2028(z.B. GGA-12345)', max_length=32, unique=True, verbose_name='Organisationskennzeichen (OKZ)')),
                ('cn', models.CharField(db_column='cn', help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK - \u2028Referat nationale und internationale Koordination)', max_length=64, verbose_name='Bezeichnung (cn)')),
                ('gvOuCn', models.TextField(db_column='gvOuCn', help_text='Gesamtbezeichnung der Organisationseinheit für die Anschrift ohne Adressteil. (Bundesministerium für Inneres Sektion IV / Abt.ITMS / Ref.NIK)', verbose_name='Gesamtbezeichnung (gvOuCn)')),
                ('mail', models.CharField(blank=True, db_column='mail', help_text='RFC 822 [RFC882] E-Mail-Adresse \u2028(helpdesk@xyz.gv.at)', max_length=256, null=True)),
                ('location', models.CharField(blank=True, db_column='l', help_text='Ort', max_length=64, null=True, verbose_name='Ort (l)')),
                ('description', models.TextField(blank=True, db_column='description', help_text='Beschreibung', max_length=1024, null=True)),
                ('gvNotValidBefore', models.CharField(blank=True, db_column='gvNotValidBefore', help_text='JJJJ-MM-TT', max_length=10, null=True, verbose_name='gültig ab')),
                ('gvNotValidAfter', models.CharField(blank=True, db_column='gvNotValidAfter', help_text='Format JJJJ-MM-TT', max_length=10, null=True, verbose_name='gültig bis')),
                ('o', models.CharField(db_column='ou', help_text='Kurzbezeichnung der Organisation (z.B. BMI)', max_length=64, unique=True, verbose_name='Kurzbezeichnung (o)')),
                ('gvOuIdParent', models.ForeignKey(blank=True, db_column='gvOuIdParent', help_text='gvOuId der übergeordneten OEs (kein dn!)', null=True, on_delete=django.db.models.deletion.CASCADE, to='tnadmin.GvOrganisation', verbose_name='Übergeordnete OE; (gvOuIdParent)')),
            ],
            options={
                'verbose_name': 'Organisation',
                'verbose_name_plural': 'Organisationen',
            },
        ),
        migrations.CreateModel(
            name='GvOrgUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gvStatus', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], db_column='gvStatus', default='active', max_length=8, null=True, verbose_name='Status')),
                ('gvSource', models.CharField(blank=True, db_column='gvSource', default='', max_length=10, null=True, verbose_name='Änderung am/durch')),
                ('gvScope', models.CharField(db_column='gvScope', default='gv.at', max_length=32, null=True)),
                ('gvOuID', models.CharField(db_column='gvOuID', max_length=32, unique=True, verbose_name='Verwaltungskennzeichen (AT:VKZ)')),
                ('gvOuVKZ', models.CharField(db_column='gvOuVKZ', help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium) \u2028(z.B. GGA-12345)', max_length=32, unique=True, verbose_name='Organisationskennzeichen (OKZ)')),
                ('cn', models.CharField(db_column='cn', help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK - \u2028Referat nationale und internationale Koordination)', max_length=64, verbose_name='Bezeichnung (cn)')),
                ('gvOuCn', models.TextField(db_column='gvOuCn', help_text='Gesamtbezeichnung der Organisationseinheit für die Anschrift ohne Adressteil. (Bundesministerium für Inneres Sektion IV / Abt.ITMS / Ref.NIK)', verbose_name='Gesamtbezeichnung (gvOuCn)')),
                ('mail', models.CharField(blank=True, db_column='mail', help_text='RFC 822 [RFC882] E-Mail-Adresse \u2028(helpdesk@xyz.gv.at)', max_length=256, null=True)),
                ('location', models.CharField(blank=True, db_column='l', help_text='Ort', max_length=64, null=True, verbose_name='Ort (l)')),
                ('description', models.TextField(blank=True, db_column='description', help_text='Beschreibung', max_length=1024, null=True)),
                ('gvNotValidBefore', models.CharField(blank=True, db_column='gvNotValidBefore', help_text='JJJJ-MM-TT', max_length=10, null=True, verbose_name='gültig ab')),
                ('gvNotValidAfter', models.CharField(blank=True, db_column='gvNotValidAfter', help_text='Format JJJJ-MM-TT', max_length=10, null=True, verbose_name='gültig bis')),
                ('ou', models.CharField(db_column='ou', help_text='Kurzbezeichnung der Organisationseinheit\u2028(z.B. IV/2b)', max_length=64, unique=True, verbose_name='Kurzbezeichnung (ou)')),
                ('gvOuIdParent', models.ForeignKey(blank=True, db_column='gvOuIdParent', help_text='gvOuId der übergeordneten OEs (kein dn!)', null=True, on_delete=django.db.models.deletion.CASCADE, to='tnadmin.GvOrgUnit', verbose_name='Übergeordnete OE; (gvOuIdParent)')),
            ],
            options={
                'verbose_name': 'Organisationseinheit',
                'verbose_name_plural': 'Organisationseinheiten',
            },
        ),
        migrations.CreateModel(
            name='GvUserPortal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gvStatus', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], db_column='gvStatus', default='active', max_length=8, null=True, verbose_name='Status')),
                ('gvSource', models.CharField(blank=True, db_column='gvSource', default='', max_length=10, null=True, verbose_name='Änderung am/durch')),
                ('gvScope', models.CharField(db_column='gvScope', default='gv.at', max_length=32, null=True)),
                ('cn', models.CharField(help_text='Eindeutige Bezeichnung des Stammportals im Email-Format (pvpportal@noel.gv.at)', max_length=64, unique=True, verbose_name='Bezeichnung')),
                ('gvMaxSecClass', models.PositiveIntegerField(help_text='Maximale gvSecClass, die Benutzer eines Portal erreichen können (z.B. 0). Anwendungsfälle sind vor Allem Test- und Entwicklungsportale. ', validators=[django.core.validators.MaxValueValidator(3)], verbose_name='Max Sicherheitsklasse')),
                ('description', models.TextField(blank=True, help_text='Beschreibung', max_length=1024, null=True)),
                ('gvFederationNames', models.ManyToManyField(to='tnadmin.GvFederation')),
                ('gvOuIdOwner', models.ForeignKey(blank=True, help_text='gvOuId des Stammportalbetreibers (Organisation des Portalverantwortlichen', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Portalbetreiber', to='tnadmin.GvOrganisation', verbose_name='Portalbetreiber')),
                ('gvOuIdParticipant', models.ForeignKey(blank=True, help_text='Liste der zugriffsberechtigten Stelle (gvOrganisation), die das Stammportal benutzen, als gvOuId', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Participant', to='tnadmin.GvOrganisation', verbose_name='Participant')),
            ],
            options={
                'verbose_name': 'Stammportal',
                'verbose_name_plural': 'Stammportale',
            },
        ),
    ]