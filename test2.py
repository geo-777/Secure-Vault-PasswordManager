import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",    # Replace with your MySQL host (e.g., 'localhost')
    user="root",  # Replace with your MySQL username
    password="password",  # Replace with your MySQL password
    database="text"  # The database you're working with
)

cursor = conn.cursor()

# Create the 'supplier' table
create_supplier_table_query = """
CREATE TABLE IF NOT EXISTS supplier (
    supplier_code INT PRIMARY KEY,
    supplier_name VARCHAR(100),
    email VARCHAR(50),
    contact_number VARCHAR(15)
)
"""
cursor.execute(create_supplier_table_query)

# Create the 'store' table
create_store_table_query = """
CREATE TABLE IF NOT EXISTS store (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100),
    item_no INT,
    qty INT,
    price DECIMAL(10, 2),
    rate DECIMAL(10, 2),
    supplier_code INT,
    FOREIGN KEY (supplier_code) REFERENCES supplier(supplier_code)
)
"""
cursor.execute(create_store_table_query)

# Insert 10 sample entries into the 'supplier' table
insert_supplier_query = """
INSERT INTO supplier (supplier_code, supplier_name, email, contact_number)
VALUES (%s, %s, %s, %s)
"""

supplier_data = [
    (1, 'Supplier A', 'supplierA@example.com', '0987654321'),
    (2, 'Supplier B', 'supplierB@example.com', '0987654322'),
    (3, 'Supplier C', 'supplierC@example.com', '0987654323'),
    (4, 'Supplier D', 'supplierD@example.com', '0987654324'),
    (5, 'Supplier E', 'supplierE@example.com', '0987654325'),
    (6, 'Supplier F', 'supplierF@example.com', '0987654326'),
    (7, 'Supplier G', 'supplierG@example.com', '0987654327'),
    (8, 'Supplier H', 'supplierH@example.com', '0987654328'),
    (9, 'Supplier I', 'supplierI@example.com', '0987654329'),
    (10, 'Supplier J', 'supplierJ@example.com', '0987654300')
]

# Insert entries into the supplier table
cursor.executemany(insert_supplier_query, supplier_data)

# Insert 10 sample entries into the 'store' table
insert_store_query = """
INSERT INTO store (item_name, item_no, qty, price, rate, supplier_code)
VALUES (%s, %s, %s, %s, %s, %s)
"""

store_data = [
    ('Item A', 101, 50, 10.99, 12.99, 1),
    ('Item B', 102, 30, 15.49, 17.49, 2),
    ('Item C', 103, 20, 8.75, 10.25, 3),
    ('Item D', 104, 15, 25.00, 27.00, 4),
    ('Item E', 105, 10, 12.50, 14.00, 5),
    ('Item F', 106, 5, 22.00, 24.00, 6),
    ('Item G', 107, 40, 7.80, 9.50, 7),
    ('Item H', 108, 25, 18.90, 20.00, 8),
    ('Item I', 109, 35, 16.25, 17.75, 9),
    ('Item J', 110, 12, 9.99, 11.50, 10)
]

# Insert entries into the store table
cursor.executemany(insert_store_query, store_data)

# Commit the changes to the database
conn.commit()

print("Tables 'store' and 'supplier' created, and 10 entries inserted successfully into each.")

# Close the connection
cursor.close()
conn.close()
