from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 5
ticket = 'T321130'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE cu_changes  ADD COLUMN IF NOT EXISTS (`cuc_private` MEDIUMBLOB default NULL);"""

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
    if 'cu_changes' not in db.run_sql('show tables;'):
        return True
    return 'cuc_private' in db.run_sql('desc cu_changes;')

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
