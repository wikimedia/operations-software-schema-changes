from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T299827'

# Don't add set session sql_log_bin=0;
command = """use centralauth;ALTER TABLE globalblocks ADD  gb_by_central_id INT UNSIGNED DEFAULT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = False

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's7'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    if 'globaluser' not in db.run_sql('use centralauth;show tables;'):
        return True
    return 'gb_by_central_id' in db.run_sql('use centralauth;desc globalblocks;')

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
