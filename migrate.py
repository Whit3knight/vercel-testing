import mysql.connector

# Credentials from screenshot
config = {
    'host': 'usfhz9.h.filess.io',
    'user': 'tugasweb_cuttingyet',
    'password': 'd41e513c1ef09b9383839096ebd93de84895c1e6',
    'database': 'tugasweb_cuttingyet',
    'port': 3306
}

try:
    print("Connecting to remote database...")
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Create table
    print("Creating table mahasiswa...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mahasiswa (
        nim VARCHAR(15) PRIMARY KEY,
        nama VARCHAR(50),
        asal VARCHAR(30)
    )
    ''')

    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM mahasiswa')
    count = cursor.fetchone()[0]

    if count == 0:
        print("Inserting sample data...")
        # Insert data
        sql = "INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)"
        values = [
            ('18.83.1233', 'Salsabila', 'Bantul'),
            ('18.83.1234', 'Rahmadi', 'Sleman'),
            ('18.83.1235', 'Sukarwo', 'Kulon Progo'),
            ('18.83.1236', 'Pambudi', 'Kulon Progo'),
            ('18.83.1237', 'Putri Amalia', 'Yogyakarta'),
            ('24.83.1125', 'Arham', 'Surabaya')
        ]
        cursor.executemany(sql, values)
        db.commit()
        print("Data inserted successfully.")
    else:
        print("Data already exists. Skipping insertion.")

    cursor.close()
    db.close()
    print("Migration finished successfully!")

except Exception as e:
    print(f"Error during migration: {e}")
