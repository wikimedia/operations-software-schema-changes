from auto_schema.schema_change import SchemaChange

# Set to None or 0 to skip downtiming
downtime_hours = 8
ticket = 'T255174'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE echo_unread_wikis MODIFY euw_wiki VARCHAR(64) NOT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = 'wikishared'

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 'x1'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    query_res = db.run_sql('use wikishared; desc echo_unread_wikis;')
    if not query_res:
        # Dry run
        return True
    field_def = query_res.split('euw_wiki')[1].split('\n')[0]
    return '64' in field_def.lower()

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
