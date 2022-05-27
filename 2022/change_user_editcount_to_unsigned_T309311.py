from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T60674'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  /*_*/user
CHANGE  user_editcount user_editcount INT UNSIGNED DEFAULT NULL;;"""

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
    query_res = db.run_sql('desc user;')
    if not query_res:
        # Dry run
        return True
    field_def = query_res.split('user_editcount')[1].split('\n')[0]
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
