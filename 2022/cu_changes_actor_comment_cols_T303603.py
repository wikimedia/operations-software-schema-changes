from auto_schema.schema_change import SchemaChange

# Set to None or 0 to skip downtiming
downtime_hours = 6
ticket = 'T303603'

# Don't add set session sql_log_bin=0;
command = """ALTER TABLE /*_*/cu_changes
    ADD COLUMN cuc_actor bigint unsigned NOT NULL DEFAULT 0 AFTER cuc_user_text,
    ADD COLUMN cuc_comment_id bigint unsigned NOT NULL DEFAULT 0 AFTER cuc_comment;
CREATE INDEX /*i*/cuc_actor_ip_time ON /*_*/cu_changes (cuc_actor, cuc_ip, cuc_timestamp);"""

# Set this to false if you don't want to run on all dbs
# In that case, you have to specify the db in the command and check function.
all_dbs = True

# DO NOT FORGET to set the right port if it's not 3306
# Use None instead of [] to get all direct replicas of master of active dc
replicas = None
section = 's5'

# The check function must return true if schema change is applied
# or not needed, False otherwise.

def check(db):
    res = db.run_sql(f'''select column_name from information_schema.columns where
        table_schema="{db.db_name}" and
        table_name="cu_changes" and
        column_name="cuc_actor"
    ''')
    return res == "cuc_actor"

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
