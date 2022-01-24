from auto_schema.schema_change import SchemaChange

# Copy this file and make adjustments

section = 's7'
should_depool = 'auto'
downtime_hours = 6
should_downtime = True
ticket = 'T299827'

# Don't add set session sql_log_bin=0;
command = """use centralauth;ALTER TABLE globalblocks ADD  gb_by_central_id INT UNSIGNED DEFAULT NULL;"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command.
all_dbs = False

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all pooled replicas
replicas = None

# Should return true if schema change is applied


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
    downtime_hours=downtime_hours,
    should_depool=should_depool
)
schema_change.run()
