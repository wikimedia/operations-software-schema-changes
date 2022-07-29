from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T314087'

# Don't add set session sql_log_bin=0;
command = """use testwiki; alter table cx_translators drop key cx_translation_translators,
add PRIMARY KEY (translator_user_id, translator_translation_id);"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = False

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's3'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    return 'cx_translation_translators' not in db.run_sql('use testwiki; show index from cx_translators;')

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
