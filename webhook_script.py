import psycopg2

def webhook_script(user_hash_id):
    conn = psycopg2.connect(
        database="testdb", 
        user="read_user", 
        password="read_user", 
        host="20.219.159.30", 
        port='5431'
    )

    cur = conn.cursor()

    # SQL to create the function
    create_function_sql = f"""
    CREATE OR REPLACE FUNCTION notify_specific_new_entry()
    RETURNS trigger AS $$
    DECLARE
    BEGIN
    IF NEW.user_hash_id = '{user_hash_id}' THEN
        PERFORM pg_notify('new_entry', row_to_json(NEW)::text);
    END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    # SQL to create the trigger for both INSERT and UPDATE events
    create_trigger_sql = """
    CREATE TRIGGER new_entry_or_update
    AFTER INSERT OR UPDATE ON transaction_Service.txn_status_flag
    FOR EACH ROW
    EXECUTE FUNCTION notify_specific_new_entry();
    """

    # Execute the SQL commands
    cur.execute(create_function_sql)
    cur.execute(create_trigger_sql)

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

