
import pymysql


class DBmanager:
    def __init__(self, host, user, port, passwd, dbname):
        # Connect to Local MYSQL DB
        self.db_name = dbname
        self.db_conn = pymysql.connect(host = host, user=user, port = port, passwd = passwd, charset="utf8") # connection to mysql
        self.cursor = self.get_new_cursor()
        print("Connection to MYSQL Done")
        
        self.check_db_exist(dbname) # name must be unique
        print("DB Existence Check Done")

        # Table User Check
        self.check_table_user()
        print("Table user Existence Check Done")


    def get_conn(self,):
        return self.db_conn
    
    def get_cursor(self,):
        return self.cursor
    
    def get_new_cursor(self,):
        try:
            cursor = self.db_conn.cursor()
            return cursor
        except  pymysql.err.InternalError as e:
            print(f"Error while getting cursor: {e}")


    def check_db_exist(self, db_name):
        self.cursor.execute(f"SHOW DATABASES LIKE '{db_name}';") # name must be unique
        result = self.cursor.fetchone()

        if not result: # No such db -> Create Database
            self.cursor.execute(f"CREATE DATABASE '{db_name}';")
            self.cursor.commit()
            print(f"Database {db_name} is created successfully")
        else :
            print(f"Database {db_name} is already created")
        
        self.cursor.execute(f"USE {self.db_name};")
        return


    def check_table_user(self,):
        self.cursor.execute(f"SHOW TABLES LIKE 'user'")
        result = self.cursor.fetchone()
        
        if not result:
            create_user_table_query = """
            CREATE TABLE user (
                user_id VARCHAR(30) PRIMARY KEY,
                password VARCHAR(300),
                name VARCHAR(20),
                belong VARCHAR(50)
            )"""

            try :
                self.cursor.execute(create_user_table_query)
                print("Create Table user Successfully")
            
            except Exception as e:
                print(f"Create Table user ERROR : {e}")

        else :
             print("Table usser already Exists")
        
        return 


    def __del__(self,):
        if self.db_conn:
            self.db_conn.close() # close connection