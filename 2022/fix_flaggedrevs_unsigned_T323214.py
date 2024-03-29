from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 24
ticket = 'T323214'

# Don't add set session sql_log_bin=0;
command = """
ALTER TABLE  /*_*/flaggedpages
CHANGE fp_page_id fp_page_id INT UNSIGNED NOT NULL,
CHANGE fp_stable fp_stable INT UNSIGNED NOT NULL;

ALTER TABLE  /*_*/flaggedrevs
CHANGE fr_page_id fr_page_id INT UNSIGNED NOT NULL,
CHANGE fr_rev_id fr_rev_id INT UNSIGNED NOT NULL;

ALTER TABLE  /*_*/flaggedtemplates
CHANGE ft_rev_id ft_rev_id INT UNSIGNED NOT NULL,
CHANGE ft_tmp_rev_id ft_tmp_rev_id INT UNSIGNED NOT NULL;

ALTER TABLE  /*_*/flaggedrevs_tracking
CHANGE ftr_from ftr_from INT UNSIGNED DEFAULT 0 NOT NULL;

ALTER TABLE  /*_*/flaggedrevs_promote
CHANGE frp_user_id frp_user_id INT UNSIGNED NOT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's5'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    if 'flaggedrevs_promote' not in db.run_sql('show tables;'):
        return True
    query_res = db.run_sql('desc flaggedrevs_promote;')
    field_def = query_res.split('frp_user_id')[1].split('\n')[0]
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
