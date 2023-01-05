from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 4
ticket = 'T326156'

# Don't add set session sql_log_bin=0;
command = """use enwikivoyage;
Alter table revsrc
MODIFY COLUMN revsrc_revid INT UNSIGNED NOT NULL,
MODIFY COLUMN revsrc_srcworkid INT UNSIGNED NOT NULL,
MODIFY COLUMN revsrc_user INT UNSIGNED NOT NULL,
MODIFY COLUMN revsrc_user_text TEXT NOT NULL;

Alter table srcwork
MODIFY COLUMN srcwork_creator INT UNSIGNED NOT NULL,
MODIFY COLUMN srcwork_site INT UNSIGNED NOT NULL;

Alter table swauthor
MODIFY COLUMN swa_site INT UNSIGNED NOT NULL;

Alter table swauthor_links
MODIFY COLUMN swal_authorid INT UNSIGNED NOT NULL,
MODIFY COLUMN swal_srcworkid INT UNSIGNED NOT NULL;

Alter table swsite
MODIFY COLUMN sws_site_uri VARBINARY(255) NOT NULL,
MODIFY COLUMN sws_work_uri VARBINARY(255) NOT NULL,
MODIFY COLUMN sws_user_uri VARBINARY(255) NOT NULL;

Alter table swsource_links
MODIFY COLUMN swsl_comment VARBINARY(255) DEFAULT '' NOT NULL,
MODIFY COLUMN swsl_workid INT UNSIGNED NOT NULL,
MODIFY COLUMN swsl_sourceid INT UNSIGNED NOT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = False

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's5'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    query_res = db.run_sql('use enwikivoyage; desc revsrc;')
    field_def = query_res.split('revsrc_user')[1].split('\n')[0]
    return 'unsigned' in field_def.lower()

schema_change = SchemaChange(
    replicas=replicas,
    section=section,
    all_dbs=all_dbs,
    check=check,
    command=command,
    ticket=ticket,
    downtime_hours=downtime_hours
)
schema_change.run()
