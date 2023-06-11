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
        sslrootcert=.postgresql/root.crt
    """)

    return conn

def logs_pg_connection():
    conn = psycopg2.connect("""
        host=rc1a-mxoodqvw58cvt97d.mdb.yandexcloud.net,rc1b-4ny0b4t0wrstwjaj.mdb.yandexcloud.net
        port=6432
        sslmode=verify-full
        dbname=points
        user=hse-ilya
        password=12345678
        target_session_attrs=read-write
        sslrootcert=../.postgresql/root.crt
    """)

    return conn