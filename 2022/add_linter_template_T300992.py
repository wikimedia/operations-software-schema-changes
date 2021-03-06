from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T300992'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE  /*_*/linter
ADD  linter_template VARBINARY(255) DEFAULT '' NOT NULL,
ADD  linter_tag VARBINARY(32) DEFAULT '' NOT NULL;
CREATE INDEX linter_cat_template ON  /*_*/linter (linter_cat, linter_template);
CREATE INDEX linter_cat_tag ON  /*_*/linter (linter_cat, linter_tag);"""

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
    if 'linter' not in db.run_sql('show tables;'):
        return True
    return 'linter_template' in db.run_sql('desc linter;')

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
