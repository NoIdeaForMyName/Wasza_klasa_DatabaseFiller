import psycopg2

import generators

conn = psycopg2.connect("dbname=Wasza_klasa user=postgres password=postgres")
cursor = conn.cursor()

profiles = generators.profiles()
for profile in profiles:
    cursor.execute(f"INSERT INTO Profiles ({', '.join(profile.keys())}) VALUES ({', '.join(['%s' for _ in range(len(profile))])})", list(profile.values()))

conn.commit()
cursor.close()
conn.close()
