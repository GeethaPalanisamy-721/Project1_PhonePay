# Connect Aggregation
import pymysql
import pandas as pd

# Read CSV files generated from ExtractAggr.py
fd_insurance = pd.read_csv('insurance_aggr.csv')
fd_transaction = pd.read_csv('transaction_aggr.csv')
fd_user = pd.read_csv('user_aggr.csv')


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
CREATE TABLE IF NOT EXISTS insurance_aggr (
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    Transaction_type VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);
"""
cursor.execute(create_insurance_table)
conn.commit()

# Insert data into insurance table
for i, row in fd_insurance.iterrows():
    sql = """
    INSERT INTO insurance_aggr (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("Insurance data inserted successfully.")

# transaction_table
create_transaction_table = """
CREATE TABLE IF NOT EXISTS transaction_aggr (
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    Transaction_type VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);
"""
#MT = fd_transaction['Transaction_count'].max()
#print(MT), count is high, so it is changed as bigint
cursor.execute(create_transaction_table)
conn.commit()

for i, row in fd_transaction.iterrows():
    sql = """
    INSERT INTO transaction_aggr (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("Transaction data inserted successfully.")

# user_tble
create_user_table = """
CREATE TABLE IF NOT EXISTS user_aggr (
    State VARCHAR(255),
    Year VARCHAR(10),
    Quarter INT,
    Brand VARCHAR(255),
    Count INT,
    Percentage FLOAT
);
"""
cursor.execute(create_user_table)
conn.commit()

for i, row in fd_user.iterrows():
    sql = """
    INSERT INTO user_aggr (State, Year, Quarter, Brand, Count, Percentage)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, tuple(row))
conn.commit()
print("User data inserted successfully.")

# Close connection
cursor.close()
conn.close()
print(" MySQL connection closed.")
