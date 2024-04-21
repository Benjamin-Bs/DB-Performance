from faker import Faker
from pymongo import MongoClient
import mysql.connector
import time

fake = Faker()

# Mongo:
mongo_client = MongoClient("mongodb://root:example@localhost:27018/")
mongo_db = mongo_client["Performance"]
mongo_collection = mongo_db["test"]
mongo_collection.create_index([('email', 1)])

# MySQL:
mysql_config = {
    'user': 'root',
    'password': 'example',
    'host': 'localhost',
    'database': 'Performance',
    'port': 3307
}
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("CREATE INDEX idx_email ON test (email)")

# Anzahl der Datensätze
num_records = 1000000

# MongoDB: Batch-Insert-Größe
mongo_batch_size = 1000

# MySQL: Batch-Insert-Größe
mysql_batch_size = 1000

def generate_data():
    data = []
    for _ in range(num_records):
        name = fake.name()
        address = fake.address()
        email = fake.email()
        city = fake.city()
        country = fake.country()
        data.append((name, address, email, city, country))
    return data

def insert_into_mongodb(data):
    mongo_collection.insert_many(data)

def insert_into_mysql(data):
    query = "INSERT INTO test (name, address, email, city, country) VALUES (%s, %s, %s, %s, %s)"
    mysql_cursor.executemany(query, data)
    mysql_conn.commit()

start_time_mongodb = time.time()
data = generate_data()
for i in range(0, num_records, mongo_batch_size):
    insert_into_mongodb(data[i:i+mongo_batch_size])
end_time_mongodb = time.time()
mongo_time = end_time_mongodb - start_time_mongodb
print("Time taken to insert into MongoDB:", mongo_time, "seconds")

start_time_mysql = time.time()
data = generate_data()
for i in range(0, num_records, mysql_batch_size):
    insert_into_mysql(data[i:i+mysql_batch_size])
end_time_mysql = time.time()
mysql_time = end_time_mysql - start_time_mysql
print("Time taken to insert into MySQL:", mysql_time, "seconds")

mongo_client.close()
mysql_cursor.close()
mysql_conn.close()
