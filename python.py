import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS stock_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        transaction_type TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

conn.commit()

# Functions for Inventory Management System

def add_product():
    name = input("Enter product name: ")
    description = input("Enter product description: ")
    price = float(input("Enter product price: "))
    category = input("Enter product category: ")
    quantity = int(input("Enter product quantity: "))

    c.execute('''
        INSERT INTO products (name, description, price, category, quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, category, quantity))
    conn.commit()
    print("Product added successfully!")

def view_products():
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    if not products:
        print("No products found.")
    else:
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Price: {product[3]}, Category: {product[4]}, Quantity: {product[5]}")

def update_product():
    product_id = int(input("Enter product ID to update: "))
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    if product:
        print(f"Current details: {product}")
        name = input(f"Enter new name (current: {product[1]}): ") or product[1]
        description = input(f"Enter new description (current: {product[2]}): ") or product[2]
        price = float(input(f"Enter new price (current: {product[3]}): ")) or product[3]
        category = input(f"Enter new category (current: {product[4]}): ") or product[4]
        quantity = int(input(f"Enter new quantity (current: {product[5]}): ")) or product[5]

        c.execute('''
            UPDATE products
            SET name=?, description=?, price=?, category=?, quantity=?
            WHERE id=?
        ''', (name, description, price, category, quantity, product_id))
        conn.commit()
        print("Product updated successfully!")
    else:
        print("Product not found!")

def delete_product():
    product_id = int(input("Enter product ID to delete: "))
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    if product:
        c.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        print("Product deleted successfully!")
    else:
        print("Product not found!")

def add_stock():
    product_id = int(input("Enter product ID to add stock: "))
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    if product:
        quantity = int(input("Enter quantity to add: "))

        c.execute('''
            UPDATE products
            SET quantity = quantity + ?
            WHERE id = ?
        ''', (quantity, product_id))

        c.execute('''
            INSERT INTO stock_transactions (product_id, quantity, transaction_type)
            VALUES (?, ?, ?)
        ''', (product_id, quantity, 'add'))
        conn.commit()
        print("Stock added successfully!")
    else:
        print("Product not found!")

def reduce_stock():
    product_id = int(input("Enter product ID to reduce stock: "))
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    if product:
        quantity = int(input("Enter quantity to reduce: "))
        if product[5] >= quantity:
            c.execute('''
                UPDATE products
                SET quantity = quantity - ?
                WHERE id = ?
            ''', (quantity, product_id))

            c.execute('''
                INSERT INTO stock_transactions (product_id, quantity, transaction_type)
                VALUES (?, ?, ?)
            ''', (product_id, quantity, 'reduce'))
            conn.commit()
            print("Stock reduced successfully!")
        else:
            print("Insufficient stock!")
    else:
        print("Product not found!")

def record_sale():
    product_id = int(input("Enter product ID to record sale: "))
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    if product:
        quantity = int(input("Enter quantity sold: "))
        if product[5] >= quantity:
            total_price = product[3] * quantity

            c.execute('''
                UPDATE products
                SET quantity = quantity - ?
                WHERE id = ?
            ''', (quantity, product_id))

            c.execute('''
                INSERT INTO sales (product_id, quantity, total_price)
                VALUES (?, ?, ?)
            ''', (product_id, quantity, total_price))
            conn.commit()
            print("Sale recorded successfully!")
        else:
            print("Insufficient stock!")
    else:
        print("Product not found!")

def view_sales():
    c.execute('SELECT * FROM sales')
    sales = c.fetchall()
    if not sales:
        print("No sales found.")
    else:
        for sale in sales:
            print(f"ID: {sale[0]}, Product ID: {sale[1]}, Quantity: {sale[2]}, Total Price: {sale[3]}, Timestamp: {sale[4]}")

def main():
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Add Stock")
        print("6. Reduce Stock")
        print("7. Record Sale")
        print("8. View Sales")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            add_stock()
        elif choice == '6':
            reduce_stock()
        elif choice == '7':
            record_sale()
        elif choice == '8':
            view_sales()
        elif choice == '9':
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

# Close the connection
conn.close()
