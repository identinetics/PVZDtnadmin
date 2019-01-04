DROP TABLE    "tnadmin_gvfederation";
DROP TABLE    "tnadmin_ldapsyncerror";
DROP TABLE    "tnadmin_ldapsyncjob";
DROP TABLE    "tnadmin_gvfederationorg";
DROP TABLE    "tnadmin_gvuserportal_gvouid_participant";
DROP TABLE    "tnadmin_gvuserportal" CASCADE;
DROP TABLE    "tnadmin_gvorganisation" CASCADE;

-- then run migrate tnadmin zero, or delete migration history from DB:
DELETE FROM django_migrations WHERE app = 'tnadmin';