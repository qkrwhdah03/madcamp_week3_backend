
# API 실행 결과 값 CODE
TRUE = "True" # On Success
FALSE = "False" # On Failure
ERROR = "Error" # Wrong with Server

class APImanager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def API_login(self, user_id, password):
        # 로그인 정보가 있는지 확인해서 확인 코드 반환
        search_query = f"""
        SELECT * 
        FROM user
        WHERE user_id = '{user_id}' AND password = '{password}';
        """
        try :
            cursor = self.db_manager.get_cursor()
            cursor.execute(search_query)
            result = cursor.fetchone() # WE have to ensure that there is unique user_id..
            
            if result:
                return TRUE
            else :
                return FALSE
            
        except Exception as e :
            print(f"Error in API_login : {e}")
            return ERROR
        
    def API_register(self, user_id, password, name, belong):
        save_register_query = f"""INSERT INTO user(user_id, password, name, belong) 
        VALUES('{user_id}', '{password}', '{name}', '{belong}')
        """
        try :
            cursor = self.db_manager.get_cursor()
            cursor.execute(save_register_query)

            self.db_manager.get_conn().commit()

            return TRUE
        except Exception as e:
            print(f"Error in API_register : {e}")
            return ERROR
        
    def API_get_profile(self, user_id):
        get_profile_query = f"""SELECT * FROM user WHERE user_id = '{user_id}';"""
        try : 
            cursor = self.db_manager.get_cursor()
            cursor.execute(get_profile_query)
            result = cursor.fetchone()

            if result:
                # 결과 반환형태에 맞도록 아마 json string?
                return str(result)
            else :
                print("Error in API_get_profile no such value")
                return ERROR
        except Exception as e :
            print("Error in API_get_profile : {e}")
            return ERROR

        
        