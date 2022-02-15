from auto_schema.schema_change import SchemaChange

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T300774'

# Don't add set session sql_log_bin=0;
command = """DROP INDEX IF EXISTS fr_img_sha1 ON /*_*/flaggedrevs;
ALTER TABLE /*_*/flaggedrevs
DROP COLUMN IF EXISTS fr_img_name,
DROP COLUMN IF EXISTS fr_img_timestamp,
DROP COLUMN IF EXISTS fr_img_sha1;"""

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
    if 'flaggedrevs' not in db.run_sql('show tables;'):
        return True
    query_res = db.run_sql('desc flaggedrevs;')
    return "fr_img_sha1" not in query_res.split()

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
