from faker import Faker
from pymongo import MongoClient
import mysql.connector
import time

fake = Faker()

# Mongo:
mongo_client = MongoClient("mongodb://root:example@localhost:27018/")
mongo_db = mongo_client["Performance"]
mongo_collection = mongo_db["test"]

# MySQL:
# Verbindungsinformationen für MySQL
mysql_config = {
    'user': 'root',
    'password': 'example',
    'host': 'localhost',
    'database': 'Performance',
    'port': 3307
}
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# MongoDB Indizes erstellen
mongo_collection.create_index([("name", 1)])
mongo_collection.create_index([("address", 1)])
mongo_collection.create_index([("email", 1)])
mongo_collection.create_index([("city", 1)])
mongo_collection.create_index([("country", 1)])

# MySQL Indizes erstellen
mysql_cursor.execute("CREATE INDEX idx_name ON test (name)")
mysql_cursor.execute("CREATE INDEX idx_address ON test (address)")
mysql_cursor.execute("CREATE INDEX idx_email ON test (email)")
mysql_cursor.execute("CREATE INDEX idx_city ON test (city)")
mysql_cursor.execute("CREATE INDEX idx_country ON test (country)")
mysql_conn.commit()

start_time_mongodb = time.time()

# 1.000 000 Datensätze generieren und in MongoDB speichern
for _ in range(1000):
    # Daten generieren
    name = fake.name()
    address = fake.address()
    email = fake.email()
    city = fake.city()
    country = fake.country()

    # MongoDB: Datensatz einfügen
    mongo_data = {"name": name, "address": address, "email": email, "city": city, "country": country}
    mongo_collection.insert_one(mongo_data)

# Zeitmessung beenden
end_time_mongodb = time.time()
mongo_time = end_time_mongodb - start_time_mongodb
print("Time taken to insert into MongoDB:", mongo_time, "seconds")

start_time_mysql = time.time()

# 1.000 000 Datensätze generieren und in MySQL speichern
for _ in range(1000000):
    # Daten generieren
    name = fake.name()
    address = fake.address()
    email = fake.email()
    city = fake.city()
    country = fake.country()

    # MySQL: Datensatz einfügen
    mysql_cursor.execute("INSERT INTO test (name, address, email, city, country) VALUES (%s, %s, %s, %s, %s)",
                         (name, address, email, city, country))
    mysql_conn.commit()

# Zeitmessung beenden
end_time_mysql = time.time()
mysql_time = end_time_mysql - start_time_mysql
print("Time taken to insert into MySQL:", mysql_time, "seconds")

mongo_client.close()
mysql_cursor.close()
mysql_conn.close()
