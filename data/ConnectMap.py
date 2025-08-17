# Connect map

import pymysql
import pandas as pd

# Read CSV files generated from ExtractMap.py
fm_insurance = pd.read_csv('insurance_map.csv')
fm_transaction = pd.read_csv('transaction_map.csv')
fm_user = pd.read_csv('user_map.csv')

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345',
    database='db_PhonePay'
)
cursor = conn.cursor()

# Create insurance table
create_insurance_table = """
CREATE TABLE IF NOT EXISTS insurance_map(
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);
"""
cursor.execute(create_insurance_table)
conn.commit()

# Insert data into insurance table
for i, row in fm_insurance.iterrows():
    sql = """
    INSERT INTO insurance_map (State, Year, Quarter, District, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("Insurance map inserted successfully.")

 #transaction_data
create_transaction_table = """
CREATE TABLE IF NOT EXISTS transaction_map (
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(100),
    Transaction_count Bigint,
    Transaction_amount FLOAT
);
"""

cursor.execute(create_transaction_table)
conn.commit()

for i, row in fm_transaction.iterrows():
    sql = """
    INSERT INTO transaction_map (State, Year, Quarter, District, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("Transaction map inserted successfully.")


# user_data
create_user_table = """
CREATE TABLE IF NOT EXISTS user_map (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    District VARCHAR(255),
    registeredUsers BIGINT,
    AppOpens BIGINT
);
"""
cursor.execute(create_user_table)
conn.commit()

for i, row in fm_user.iterrows():
    sql = """
    INSERT INTO user_map (State, Year, Quarter, District, registeredUsers, AppOpens)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("User map inserted successfully.")

# Close connection
cursor.close()
conn.close()
print(" MySQL Mapconnection closed.")