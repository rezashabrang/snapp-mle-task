"""Data populator for postgres."""

import argparse
import ast

import geopandas as gpd
import pandas as pd
import psycopg2
from psycopg2._psycopg import connection


# Function to connect to PostgreSQL
def connect_to_postgres(host, port, database, user, password):
    conn = psycopg2.connect(
        host=host, port=port, database=database, user=user, password=password
    )
    return conn


# Function to create table and insert data
def load_ride_data_to_postgres(conn: connection, csv_file):
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Construct the query string
    insert_query = """
        INSERT INTO ride_location (latitude, longitude) VALUES (%s, %s);
    """

    # Prepare a list to hold all the values to insert
    values = []

    # # Populate the values list with tuples of data
    for _, row in df.iterrows():
        values.append((row["lat"], row["long"]))

    # Execute the query with all values in a single transaction
    cur.executemany(insert_query, values)
    conn.commit()

    # Close communication with the database
    cur.close()

    print(f"Data successfully loaded into PostgreSQL.")


# Function to create table and insert data
def load_place_data_to_postgres(conn: connection, csv_file):
    # Open a cursor to perform database operations
    cur = conn.cursor()

    gdf = gpd.read_file(csv_file)
    # Prepare data for insertion
    for _, row in gdf.iterrows():
        # Extract data from GeoDataFrame
        name = row["name"]
        original_polygon = row["original_polygon"]
        entrances = ast.literal_eval(row["entrances"])
        # Convert entrances to a PostgreSQL array of POINT
        entrances_array = [
            f"ST_GeomFromText('POINT({lng} {lat})', 4326)" for lat, lng in entrances
        ]
        entrances_array_str = f"ARRAY[{','.join(entrances_array)}]"
        print(entrances_array_str)

        # Construct and execute INSERT statement
        insert_query = f"""
            INSERT INTO place_meta (name, polygon, entrances)
            VALUES (%s, ST_GeomFromText(%s, 4326), {entrances_array_str});
        """
        print(insert_query)
        cur.execute(insert_query, (name, original_polygon))

    # Commit the transaction
    conn.commit()

    # Close communication with the database
    cur.close()

    print(f"Data successfully loaded into PostgreSQL.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load CSV data into PostgreSQL")
    parser.add_argument("--host", type=str, required=True, help="PostgreSQL host")
    parser.add_argument("--port", type=str, default="5432", help="PostgreSQL port")
    parser.add_argument(
        "--database", type=str, required=True, help="PostgreSQL database name"
    )
    parser.add_argument("--user", type=str, required=True, help="PostgreSQL username")
    parser.add_argument(
        "--password", type=str, required=True, help="PostgreSQL password"
    )
    parser.add_argument(
        "--csv_file", type=str, required=True, help="Path to the CSV file"
    )
    parser.add_argument("--data_type", type=str, required=True, help="ride or place")

    args = parser.parse_args()

    # Connect to PostgreSQL
    conn = connect_to_postgres(
        args.host, args.port, args.database, args.user, args.password
    )

    if args.data_type == "ride":
        # Load data into PostgreSQL
        load_ride_data_to_postgres(conn, args.csv_file)
    elif args.data_type == "place":
        load_place_data_to_postgres(conn, args.csv_file)
    else:
        raise Exception("Bad data_type argument!")

    # Close PostgreSQL connection
    conn.close()
