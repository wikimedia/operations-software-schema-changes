from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T298565'

fields = {
    'user_newpass_time': 'BINARY(14) DEFAULT NULL',
    'user_email_authenticated': 'BINARY(14) DEFAULT NULL',
    'user_email_token': 'BINARY(32) DEFAULT NULL',
    'user_email_token_expires': 'BINARY(14) DEFAULT NULL',
    'user_touched': 'BINARY(14) NOT NULL',
    'user_token': 'BINARY(32) DEFAULT \'\' NOT NULL',
    'user_registration': 'BINARY(14) DEFAULT NULL'
}

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's7'

# The check function must return true if schema change is applied
# or not needed, False otherwise.
for field in fields:
    def check(db):
        query_res = db.run_sql('desc user;')
        if not query_res:
            # Dry run
            return True
        field_def = query_res.split(field)[1].split('\n')[0]
        return 'varbinary' not in field_def.lower()

    schema_change = SchemaChange(
        replicas=replicas,
        section=section,
        all_dbs=all_dbs,
        check=check,
        command='ALTER TABLE /*_*/user CHANGE {} {} {};'.format(field, field, fields[field]),
        ticket=ticket,
        downtime_hours=downtime_hours
    )
    schema_change.run()
