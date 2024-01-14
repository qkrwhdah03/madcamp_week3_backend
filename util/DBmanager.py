
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
        table_name = "user" 
        self.check_table(table_name, f"""
            CREATE TABLE {table_name} (
                user_id VARCHAR(30) PRIMARY KEY,
                password VARCHAR(300),
                name VARCHAR(20),
                belong VARCHAR(50)
            )""")
        print(f"Table {table_name} Existence Check Done")

        # Table Project Check
        table_name = "project"
        self.check_table(table_name, f"""
            CREATE TABLE {table_name} (
                project_id INT AUTO_INCREMENT PRIMARY KEY,
                project_name VARCHAR(30),
                project_description VARCHAR(200),
                project_leader VARCHAR(30)    
            )""")
        print(f"Table {table_name} Existence Check Done")

        # Table proejct belong Check
        table_name = "project_belong"
        self.check_table(table_name, f"""
            CREATE TABLE {table_name} (
                project_id INT, 
                user_id VARCHAR(30), 
                PRIMARY KEY (project_id, user_id),
                FOREIGN KEY (project_id) REFERENCES project(project_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id)     
            )""")
        print(f"Table {table_name} Existence Check Done")

        # Todo Table Check
        table_name = "todo"
        self.check_table(table_name, f"""
            CREATE TABLE {table_name} (
                todo_id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT,
                todo VARCHAR(100),
                FOREIGN KEY(project_id) REFERENCES project(project_id)
            );""")
        print(f"Table {table_name} Existence Check Done")

        
        # Appointment Table
        table_name = "appointment"
        self.check_table(table_name, f"""
            CREATE TABLE {table_name} (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT,
                appointment VARCHAR(100),
                FOREIGN KEY(project_id) REFERENCES project(project_id)
            );""")
        print(f"Table {table_name} Existence Check Done")


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


    def check_table(self, table_name, table_create_query):
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = self.cursor.fetchone()
        
        if not result:
            try :
                self.cursor.execute(table_create_query)
                print(f"Create Table {table_name} Successfully")
            
            except Exception as e:
                print(f"Create Table {table_name} ERROR : {e}")

        else :
             print(f"Table {table_name} already Exists")
        
        return 


    def __del__(self,):
        if self.db_conn:
            self.db_conn.close() # close connection