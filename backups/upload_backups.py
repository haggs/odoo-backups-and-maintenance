#######################################################################################
#
# This script uploads the backups it finds in /opt/openerp/backups to the s3 bucket
# "altaerpbackups" under the directory specified by the conf.py file.
#
# Requirements: * s3cmd must be configured for this linux user
#               * You must have an s3 bucket called odoobackups
#               * /var/log/odoo/upload_backups.log must exist and be writeable by the linux user
#                 that executes this script.
#               * a conf.py file must be created in this directory with the following
#                 variables: SYSTEM_NAME
#               * /opt/openerp/backups must exist and be readable by the linux user that
#                 executes this script
#
# Author:       Dan Haggerty
# Date:         Feb. 16th 2015
#
#######################################################################################
import logging
import logging.handlers
from datetime import *
import subprocess
import sys


# Setup logging
log_path = '/var/log/odoo/upload_backups.log'
logger   = logging.getLogger('Upload Logger')
handler  = logging.handlers.RotatingFileHandler( log_path, maxBytes=100000, backupCount=5 )
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def timestamp():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S] ")

# Import conf.py and verify it has what it needs
try:
    sys.path.append('/opt/openerp')
    from conf import *
    assert SYSTEM_NAME
    assert DB_NAME
except Exception:
    msg = timestamp() + "Error while importing configuration file. Make sure you've made a conf.py file for this system, "\
          + "and that it contains the following variables: SYSTEM_NAME, DB_NAME"
    logger.error(msg, exc_info=True)
    raise Exception(msg)

logger.info( "\n" + timestamp()+ "=================================================================================" )
logger.info( timestamp() + "Starting upload of database backups for system: " + SYSTEM_NAME )
logger.info( timestamp() + "=================================================================================" )

# Upload the backup
try:
    logger.info( timestamp() + "Uploading database to: s3://odoobackups/" + SYSTEM_NAME + '/' )
    output = subprocess.check_output(['s3cmd sync /opt/openerp/backups/ s3://odoobackups/' + SYSTEM_NAME +'/'], shell=True)
    logger.info( timestamp() + '    Done!' )
except Exception:
    msg = timestamp() + "Error while uploading database"
    logger.error(msg, exc_info=True)
    raise Exception(msg)

logger.info(timestamp() + "=================================================================================")
logger.info(timestamp() + "Completed upload of database backups for system: " + SYSTEM_NAME)
logger.info(timestamp() + "=================================================================================")




