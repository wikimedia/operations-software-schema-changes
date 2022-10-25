from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

# Set to None or 0 to skip downtiming
downtime_hours = 24
ticket = 'T318605'

# Don't add set session sql_log_bin=0;
command = """DROP  INDEX el_from ON  /*_*/externallinks;
ALTER TABLE  /*_*/externallinks
ADD  el_to_domain_index VARBINARY(255) DEFAULT '' NOT NULL,
ADD  el_to_path BLOB DEFAULT NULL;
CREATE INDEX el_to_domain_index_to_path ON  /*_*/externallinks (    el_to_domain_index,    el_to_path(60)  );
CREATE INDEX el_from ON  /*_*/externallinks (el_from);"""

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
    return 'el_to_domain_index' in db.run_sql('desc externallinks;')

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
