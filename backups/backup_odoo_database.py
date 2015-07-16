#######################################################################################
#
# This script backups the database of an Odoo system. It first stops the running
# Odoo server process, then backs up the database, then starts the server again.
#
# Requirements: * /var/log/odoo/backup_odoo_database.log must exist and be writeable by the linux user
#                 that executes this script.
#               * a conf.py file must be created in this directory with the following
#                 variables: SYSTEM_NAME, DB_NAME
#               * /etc/init.d/openerp-server must exist and be executable by the linux user
#                 that executes this script
#               * /opt/openerp/backups must exist and be writeable by the linux user that
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
log_path = '/var/log/odoo/backup_odoo_database.log'
logger   = logging.getLogger('Backup Logger')
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
    msg = timestamp() + "Error while importing configuration file. Make sure you've made a conf.py file for this system in /opt/openerp, "\
          + "and that it contains the following variables: SYSTEM_NAME, DB_NAME"
    logger.error(msg, exc_info=True)
    raise Exception(msg)

logger.info( "\n" + timestamp()+ "=================================================================================" )
logger.info( timestamp() + "Starting Odoo database backup: " + SYSTEM_NAME )
logger.info( timestamp() + "=================================================================================" )

# Stop Odoo server
try:
    logger.info( timestamp() + "Stopping Odoo server" )
    output = subprocess.check_output(['/etc/init.d/openerp-server', 'stop'], shell=True)
    logger.info( timestamp() + '    Done!' )

except Exception:
    msg = timestamp() + "Error while stopping the odoo server"
    logger.error(msg, exc_info=True)

# Backup the database
backup_path = '/opt/openerp/backups/' + SYSTEM_NAME + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".dump"

try:
    logger.info( timestamp() + "Backing up database to: " + backup_path )
    output = subprocess.check_output(['pg_dump -E UTF-8 -p 5432 -F c -b -U openerp -w -f ' + backup_path + " " + DB_NAME], shell=True)
    logger.info( timestamp() + '    Done!' )
except Exception:
    msg = timestamp() + "Error while getting database dump"
    logger.error(msg, exc_info=True)
    raise Exception(msg) 

# Start the server
try:
    logger.info( timestamp() + "Starting Odoo server" )
    output = subprocess.check_output(['/etc/init.d/openerp-server', 'start'], shell=True)
    logger.info( timestamp() + "    Done!")
except Exception:
    msg = timestamp() + "Error while starting the odoo server"
    logger.error(msg, exc_info=True)

logger.info(timestamp() + "=================================================================================")
logger.info(timestamp() + "Completed Odoo database backup: " + SYSTEM_NAME)
logger.info(timestamp() + "=================================================================================")




