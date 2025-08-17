import pymysql
import pandas as pd

# Read CSV files
ft_insurance = pd.read_csv('insurance_top.csv')
ft_transaction = pd.read_csv('transaction_top.csv')
ft_user = pd.read_csv('user_top.csv')

# Clean insurance data
ft_insurance.fillna(0, inplace=True)
ft_insurance["Quarter"] = ft_insurance["Quarter"].astype(int)
ft_insurance["pincodes"] = ft_insurance["pincodes"].astype(int)
ft_insurance["Transaction_count"] = ft_insurance["Transaction_count"].astype(int)
ft_insurance["Transaction_amount"] = ft_insurance["Transaction_amount"].astype(int)

# Clean transaction data
ft_transaction.fillna(0, inplace=True)
ft_transaction["Quarter"] = ft_transaction["Quarter"].astype(int)
ft_transaction["pincodes"] = ft_transaction["pincodes"].astype(int)
ft_transaction["Transaction_count"] = ft_transaction["Transaction_count"].astype(int)
ft_transaction["Transaction_amount"] = ft_transaction["Transaction_amount"].astype(int)

# Clean user data
ft_user.fillna(0, inplace=True)
ft_user["Quarter"] = ft_user["Quarter"].astype(int)
ft_user["pincodes"] = ft_user["pincodes"].astype(int)
ft_user["registeredUsers"] = ft_user["registeredUsers"].astype(int)

# print columns to verify
print("Insurance Columns:", ft_insurance.columns.tolist())
print("Transaction Columns:", ft_transaction.columns.tolist())
print("User Columns:", ft_user.columns.tolist())

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='12345',
    database='db_PhonePay'
)
cursor = conn.cursor()

# 1. Create insurance_top table
cursor.execute("""
CREATE TABLE IF NOT EXISTS insurance_top(
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    pincodes BIGINT,
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);
""")
conn.commit()

# Insert into insurance_top
for i, row in ft_insurance.iterrows():
    try:
        sql = """
        INSERT INTO insurance_top (State, Year, Quarter, pincodes, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            row["State"],
            str(row["Year"]),
            int(row["Quarter"]),
            int(row["pincodes"]),
            int(row["Transaction_count"]),
            int(row["Transaction_amount"])
        )
        cursor.execute(sql, values)
    except Exception as e:
        print(f"Error inserting row {i} into insurance_top: {e}")
        print("Values:", values)
conn.commit()
print("Insurance top inserted successfully.")

# 2. Create transaction_top table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction_top(
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    pincodes BIGINT,
    Transaction_count BIGINT,
    Transaction_amount BIGINT
);
""")
conn.commit()

# Insert into transaction_top
for i, row in ft_transaction.iterrows():
    try:
        sql = """
        INSERT INTO transaction_top (State, Year, Quarter, pincodes, Transaction_count, Transaction_amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            row["State"],
            str(row["Year"]),
            int(row["Quarter"]),
            int(row["pincodes"]),
            int(row["Transaction_count"]),
            int(row["Transaction_amount"])
        )
        cursor.execute(sql, values)
    except Exception as e:
        print(f"Error inserting row {i} into transaction_top: {e}")
        print("Values:", values)
conn.commit()
print("Transaction top inserted successfully.")

# 3. Create user_top table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_top(
    State VARCHAR(150),
    Year VARCHAR(10),
    Quarter INT,
    pincodes BIGINT,
    registeredUsers BIGINT
);
""")
conn.commit()

# Insert into user_top
for i, row in ft_user.iterrows():
    try:
        sql = """
        INSERT INTO user_top (State, Year, Quarter, pincodes, registeredUsers)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            row["State"],
            str(row["Year"]),
            int(row["Quarter"]),
            int(row["pincodes"]),
            int(row["registeredUsers"])
        )
        cursor.execute(sql, values)
    except Exception as e:
        print(f"Error inserting row {i} into user_top: {e}")
        print("Values:", values)
conn.commit()
print("User top inserted successfully.")

# Close connection
cursor.close()
conn.close()
print("MySQL Top connection closed.")



