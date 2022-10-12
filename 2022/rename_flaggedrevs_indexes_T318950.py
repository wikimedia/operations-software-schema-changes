from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T318950'

# Don't add set session sql_log_bin=0;
command = """alter table flaggedrevs
drop index if exists page_rev, add key fr_page_rev (fr_page_id, fr_rev_id),
drop index if exists page_time, add key fr_page_time (fr_page_id, fr_rev_timestamp),
drop index if exists page_qal_rev, add key fr_page_qal_rev (fr_page_id,fr_quality,fr_rev_id),
drop index if exists page_qal_time, add key fr_page_qal_time (fr_page_id,fr_quality,fr_rev_timestamp);"""

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
    if 'flaggedrevs' not in db.run_sql('show tables;'):
        return True
    return 'fr_page_qal_time' in db.run_sql('show indexes from flaggedrevs;')

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
