from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 8
ticket = 'T333332'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  /*_*/abuse_filter
ADD  af_actor BIGINT UNSIGNED DEFAULT 0 NOT NULL,
CHANGE  af_user af_user BIGINT UNSIGNED DEFAULT 0 NOT NULL,
CHANGE  af_user_text af_user_text VARBINARY(255) DEFAULT '' NOT NULL;
CREATE INDEX af_actor ON  /*_*/abuse_filter (af_actor);

ALTER TABLE  /*_*/abuse_filter_history
ADD  afh_actor BIGINT UNSIGNED DEFAULT 0 NOT NULL,
CHANGE  afh_user afh_user BIGINT UNSIGNED DEFAULT 0 NOT NULL,
CHANGE  afh_user_text afh_user_text VARBINARY(255) DEFAULT '' NOT NULL;
CREATE INDEX afh_actor ON  /*_*/abuse_filter_history (afh_actor);"""

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
    if 'abuse_filter' not in db.run_sql('show tables;'):
        return True
    return 'af_actor' in db.run_sql('desc abuse_filter;')

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
