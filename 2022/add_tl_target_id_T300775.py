from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 12
ticket = 'T300775'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE templatelinks ADD  tl_target_id BIGINT UNSIGNED DEFAULT NULL;CREATE INDEX tl_target_id ON  /*_*/templatelinks (tl_target_id, tl_from);CREATE INDEX tl_backlinks_namespace_target_id ON templatelinks (tl_from_namespace, tl_target_id, tl_from);"""

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
    if 'templatelinks' not in db.run_sql('show tables;'):
        return True
    return 'tl_target_id' in db.run_sql('desc templatelinks;')

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
