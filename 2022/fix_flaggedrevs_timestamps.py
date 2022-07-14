from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 10
ticket = 'T312984'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  /*_*/flaggedpages
CHANGE  fp_pending_since fp_pending_since BINARY(14) DEFAULT NULL;
ALTER TABLE  /*_*/flaggedpage_pending
CHANGE  fpp_pending_since fpp_pending_since BINARY(14) NOT NULL;
ALTER TABLE  /*_*/flaggedrevs_statistics
CHANGE  frs_timestamp frs_timestamp BINARY(14) NOT NULL;
ALTER TABLE  /*_*/flaggedpage_config
ALTER   fpc_expiry  DROP DEFAULT;
ALTER TABLE  /*_*/flaggedrevs
CHANGE  fr_rev_timestamp fr_rev_timestamp BINARY(14) NOT NULL,
CHANGE  fr_timestamp fr_timestamp BINARY(14) NOT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's3'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    if 'flaggedpages' not in db.run_sql('show tables;'):
        return True
    query_res = db.run_sql('desc flaggedpages;')
    field_def = query_res.split('fp_pending_since')[1].split('\n')[0]
    return 'varbinary' not in field_def.lower()

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
