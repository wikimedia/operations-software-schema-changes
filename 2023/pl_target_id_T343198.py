from auto_schema.schema_change import SchemaChange

section = 's1'
downtime_hours = 24
ticket = 'T343198'

# Don't add set session sql_log_bin=0;
command = """
ALTER TABLE  /*_*/pagelinks
ADD  pl_target_id BIGINT UNSIGNED DEFAULT NULL;
CREATE INDEX pl_target_id ON  /*_*/pagelinks (pl_target_id, pl_from);
CREATE INDEX pl_backlinks_namespace_target_id ON  /*_*/pagelinks (    pl_from_namespace, pl_target_id,    pl_from  );
"""
# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all pooled replicas
replicas = None


# Should return true if schema change is applied
def check(db):
    columns = db.get_columns('pagelinks')
    return 'pl_target_id' in columns


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
