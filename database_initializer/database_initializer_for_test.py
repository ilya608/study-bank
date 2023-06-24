from database_initializer.avg_table.avg_table_initializer import PostgresAvgTableInitializer
from features_collector.postgres.postgres_connection import get_pg_connection



if __name__ == "__main__":
    pg_connection = get_pg_connection()

    # points_table = PostgresPointsTableInitializer(pg_connection)
    # points_table.create_table_points()

    avg_table = PostgresAvgTableInitializer(pg_connection)
    avg_table.create_avg_table()