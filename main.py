import psycopg2
from psycopg2 import sql
import generators

DEFAULT_DATABASE_NAME = 'postgres'
DATABASE_NAME = 'Wasza_klasa'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'

def insert_rows(cursor, rows, table_name):
    for row in rows:
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({', '.join(['%s' for _ in range(len(row))])})", list(row.values()))
    print(f'Table {table_name} filled')


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


# Reconnect to create the new database and execute further commands
conn = psycopg2.connect(f"dbname={DATABASE_NAME} user={DATABASE_USER} password={DATABASE_PASSWORD}")
cursor = conn.cursor()

# profiles = generators.profiles()
# for profile in profiles:
#     cursor.execute(f"INSERT INTO Profiles ({', '.join(profile.keys())}) VALUES ({', '.join(['%s' for _ in range(len(profile))])})", list(profile.values()))

insert_rows(cursor, generators.profiles(), 'Profiles')
insert_rows(cursor, generators.chats(), 'Chats')
insert_rows(cursor, generators.friendships(), 'Friendships')
insert_rows(cursor, generators.groups(), 'Groups')

conn.commit()

cursor.close()
conn.close()
print("Database Filled")
