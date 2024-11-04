import psycopg2
from psycopg2 import sql

import generators
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count

DEFAULT_DATABASE_NAME = 'postgres'
DATABASE_NAME = 'Wasza_klasa'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'


# def insert_rows(cursor, rows, table_name):
#     for row in rows:
#         cursor.execute(f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({', '.join(['%s' for _ in range(len(row))])})", list(row.values()))

def insert_rows(cursor, rows, table_name):
    if not rows:
        return
    columns = rows[0].keys()
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"
    values = [list(row.values()) for row in rows]
    psycopg2.extras.execute_batch(cursor, query, values)


# Connect to the default database to execute the DROP DATABASE and later CREATE DATABASE commands
conn = psycopg2.connect(f"dbname={DEFAULT_DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD}")
conn.autocommit = True  # Ensure autocommit is enabled
cursor = conn.cursor()

# Drop existing database
cursor.execute(f'DROP DATABASE IF EXISTS "{DATABASE_NAME}"')
print("Database Dropped")

# Create the new database
cursor.execute(f'CREATE DATABASE "{DATABASE_NAME}"')
print("Database Created")

cursor.close()
conn.close()


# Connect to the database to create the structure from the DDL script
conn = psycopg2.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD}")
cursor = conn.cursor()

with open('wasza_klasa_ddl.sql', 'r') as file:
    sql_script = file.read()
cursor.execute(sql_script)

conn.commit()

cursor.close()
conn.close()
print("Database structure created")


def insert_data(rows, table_name):
    try:
        # connecting with database
        with psycopg2.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD}") as conn:
            with conn.cursor() as cursor:
                # inserting rows to the table
                insert_rows(cursor,rows,table_name)
            conn.commit()  # confirming transaction
        print(f'Table {table_name} filled')
    except psycopg2.DatabaseError as e:
        print(f"Error during inserting data to the table {table_name}: {e}")


tables_and_generators = {
    'Permissions':generators.permissions,
    'Rooms':generators.rooms,
    'Roles':generators.roles,
    'Types':generators.types,
    'Extensions': generators.extensions,
    'Profiles': generators.profiles,
    'Chats': generators.chats,
    'Friendships': generators.friendships,
    'Groups': generators.groups,
    'Affiliations':generators.affiliations,
    'Posts': generators.posts,
    'Shares':generators.shares,
    'Albums':generators.albums,
    'Media':generators.media,
    'Publications':generators.publications,
    'Comments':generators.comments,
    'Reactions':generators.reactions,
    'Notifications':generators.notifications,
    'Participations':generators.participations,
}

data = {}
with ThreadPoolExecutor() as executor:
    # creating threads for generators
    futures = {table: executor.submit(generator) for table, generator in tables_and_generators.items()}

    # waiting for the results
    for table, future in futures.items():
        try:
            data[table] = future.result()  # getting generated data
        except Exception as e:
            print(f"Error generating data for {table}: {e}")

    data["Messages"]=generators.messages(data['Chats'],data["Participations"],data['Media'])
    
# Sequentially insert generated data
for table, rows in data.items():
    insert_data(rows, table)

cursor.close()
conn.close()
print("Database Filled")
