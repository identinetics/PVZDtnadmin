import logging
import subprocess

from django.conf import settings

def recreate_db():
    command1 = settings.DBADMIN_SHELL + ('-c', 'DROP DATABASE ' +  settings.DATABASES['default']['NAME'])
    command2 = settings.DBADMIN_SHELL + ('-c', 'CREATE DATABASE ' +  settings.DATABASES['default']['NAME'])
    exec(command1)
    exec(command2)


def exec(cmd_args: str):
    pipes = subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (std_out, std_err_bytes) = pipes.communicate()
    std_err = std_err_bytes.decode('utf-8').strip()
    err_msg = "{}. Returncode: {}. Command: {}".format(std_err, pipes.returncode, ' '.join(cmd_args))

    if pipes.returncode != 0:
        if not err_msg.startswith('ERROR:  database "pvzddb_unittest" does not exist'):
            raise Exception(err_msg)
    elif len(std_err):
        logging.warning(err_msg)
    else:
        logging.debug(std_out.decode('utf-8'))