import mariadb

def getConnection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password = "setia@123",
            host="127.0.0.1",
            port=3306,
            database="openhealthcareai"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
      
    return conn