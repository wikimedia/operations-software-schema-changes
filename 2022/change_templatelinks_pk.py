from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 24
ticket = 'T312863'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  /*_*/templatelinks
DROP  PRIMARY KEY;
ALTER TABLE  /*_*/templatelinks
CHANGE  tl_target_id tl_target_id BIGINT UNSIGNED NOT NULL;
ALTER TABLE  /*_*/templatelinks
ADD  PRIMARY KEY (tl_from, tl_target_id);"""

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
    query_res = db.run_sql('desc templatelinks;')
    if not query_res:
        # Dry run
        return True
    field_def = query_res.split('tl_target_id')[1].split('\n')[0]
    return 'no' not in field_def.lower()

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
