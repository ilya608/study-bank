import psycopg2


def get_pg_connection():
    conn = psycopg2.connect("""
        host=rc1a-mxoodqvw58cvt97d.mdb.yandexcloud.net,rc1b-4ny0b4t0wrstwjaj.mdb.yandexcloud.net
        port=6432
        sslmode=verify-full
        dbname=points
        user=hse-ilya
        password=12345678
        target_session_attrs=read-write
    """)

    return conn

    q.execute("SELECT application_name, client_addr, state FROM pg_stat_replication;")
    replicas = q.fetchall()

    for replica in replicas:
        application_name, client_addr, state = replica
        print(f"Application Name: {application_name}, Client Address: {client_addr}, State: {state}")

    print(q.fetchone())

    conn.close()
