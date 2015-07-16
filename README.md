
# Odoo Backups and Maintenance
This repository contains a few quick-and-dirty Python scripts that I made for a few tasks necessary in maintaining
an Odoo/OpenERP server. 

###Backups
The scripts in the "backups" directory are used for backing up an Odoo system's Postgres database, and uploading it
to a bucket in Amazon S3. Read through the comment block in "backups/backup_odoo_database.py" and "backups/upload_backups.py" for
a description of the requirements.

###Maintenance
Right now the "maintenance" directory contains just one script, "office_keepalive.py". This script is used for
keeping the openoffice service alive if it crashes. We use this for generating reports using Aeroo Reports.
