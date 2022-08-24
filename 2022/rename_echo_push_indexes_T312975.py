from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T312975'

# Don't add set session sql_log_bin=0;
command = """use wikishared;
ALTER TABLE /*_*/echo_push_subscription DROP FOREIGN KEY IF EXISTS /*_*/echo_push_subscription_ibfk_1;
ALTER TABLE /*_*/echo_push_subscription DROP FOREIGN KEY IF EXISTS /*_*/echo_push_subscription_ibfk_2;
DROP INDEX IF EXISTS /*i*/echo_push_subscription_user_id ON /*_*/echo_push_subscription;
CREATE INDEX IF NOT EXISTS /*i*/eps_user ON /*_*/echo_push_subscription (eps_user);
DROP INDEX IF EXISTS /*i*/echo_push_subscription_token ON /*_*/echo_push_subscription;
CREATE INDEX IF NOT EXISTS /*i*/eps_token ON /*_*/echo_push_subscription (eps_token(10));
"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = False

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 'x1'

# The check function must return true if schema change is applied
# or not needed, False otherwise.


def check(db):
    return 'echo_push_subscription_token' not in db.run_sql('show indexes from wikishared.echo_push_subscription;')

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
