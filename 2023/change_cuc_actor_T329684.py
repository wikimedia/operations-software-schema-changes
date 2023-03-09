from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T329684'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  cu_changes CHANGE  cuc_actor cuc_actor BIGINT UNSIGNED NOT NULL, CHANGE  cuc_comment_id cuc_comment_id BIGINT UNSIGNED NOT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's6'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    query_res = db.run_sql('show create table cu_changes;')
    if not query_res:
        # Dry run
        return True
    field_def = query_res.split('cuc_comment_id')[1].split('\n')[0]
    return 'DEFAULT' not in field_def

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
