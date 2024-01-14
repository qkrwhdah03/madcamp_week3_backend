from util.JSONconverter import JSONconverter


# API 실행 결과 값 CODE
TRUE = "True" # On Success
FALSE = "False" # On Failure
ERROR = "Error" # Wrong with Server

class APImanager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.convert = JSONconverter()

    def API_check_user(self, user_id):
        try : 
            search_query = f"""SELECT * FROM user WHERE user_id = '{user_id}'; """
            cursor = self.db_manager.get_cursor()
            cursor.execute(search_query)
            result = cursor.fetchone()
            if result:
                return TRUE
            else :
                return FALSE
            
        except Exception as e:
            print(f"Error in API_check_user : {e}")
            return ERROR

    def API_login(self, user_id, password):
        # 로그인 정보가 있는지 확인해서 확인 코드 반환
        try :
            search_query = f"""
                SELECT * 
                FROM user
                WHERE user_id = '{user_id}' AND password = '{password}';
            """
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
    
    def API_duplicate(self, user_id):
        try :
            duplicate_request = f"""SELECT * FROM user WHERE user_id ='{user_id}';"""
            cursor = self.db_manager.get_cursor()
            cursor.execute(duplicate_request)
            result = cursor.fetchone()

            if result:
                return FALSE
            else :
                return TRUE
            
        except Exception as e:
            print(f"Error in API_duplicate : {e}")
            return ERROR


    def API_register(self, user_id, password, name, belong):
        try :
            save_register_query = f"""INSERT INTO user(user_id, password, name, belong) 
            VALUES('{user_id}', '{password}', '{name}', '{belong}')
            """
            cursor = self.db_manager.get_cursor()
            cursor.execute(save_register_query)

            self.db_manager.get_conn().commit()

            return TRUE
        except Exception as e:
            print(f"Error in API_register : {e}")
            self.db_manager.get_conn().rollback()
            return ERROR
        
    def API_get_profile(self, user_id):
        # User Table
        try : 
            get_profile_query = f"""SELECT * FROM user WHERE user_id = '{user_id}';"""
            cursor = self.db_manager.get_cursor()
            cursor.execute(get_profile_query)
            user_info_result = cursor.fetchone()

            if not user_info_result:
                print("Error in API_get_profile no such value")
                return ERROR
        
            # Get Project id
            get_project_list_query = f"""SELECT * FROM project_belong WHERE user_id = '{user_id}';"""

            cursor = self.db_manager.get_cursor()
            cursor.execute(get_project_list_query)
            result = cursor.fetchall() # 한 명이 여러 개의 프로젝트도 가능
            
            project_list = []
            teammate_list = []
            
            for row in result:
                project_id = row[0] # project_belong의 project_id index
                get_project_info_query = f"""SELECT * FROM project WHERE project_id = {str(project_id)};"""
                cursor.execute(get_project_info_query)
                project = cursor.fetchone()  # project_id is PK
                project_list.append(project)
                #print(project)
                
                # Get Project Team
                get_project_team_query =f"""SELECT * FROM project_belong WHERE project_id = '{str(project_id)}';"""
                cursor.execute(get_project_team_query)
                team = cursor.fetchall() # 팀은 여러 명 가능
                #print(team)
                teammate = []
                for team_user in team:
                    teammate.append(team_user[1])  # project_belong의 user_id index
                teammate_list.append(teammate)

            return self.convert.convert_profile_info(user_info_result, project_list, teammate_list)

        except Exception as e:
            print(f"Error in API_get_Profile : {e}")
            return ERROR   
        
    def API_register_project(self, name, leader, description, team_list): # Project Leader 추가하기 - 받아와야함
        try :
            query = f"""INSERT INTO project(project_name, project_description, project_leader) VALUES('{name}', '{description}','{leader}');"""
            cursor = self.db_manager.get_cursor()
            cursor.execute(query)
            
            project_id = cursor.lastrowid 
            
            if project_id == None:
                raise Exception("Fail to get project_id")

            # project_belong Table에 team_list 추가
            for team in team_list:
                query = f"""INSERT INTO project_belong(project_id, user_id) VALUES({str(project_id)},'{team}');"""
                cursor.execute(query)

            self.db_manager.get_conn().commit()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_register-project : {e}")
            self.db_manager.get_conn().rollback()
            return ERROR
        
    def API_delete_project(self, project_id):
        try :
            query = f"""DELETE FROM project_belong WHERE project_id = {str(project_id)};"""
            cursor = self.db_manager.get_cursor()
            cursor.execute(query)

            query = f"""DELETE FROM project WHERE project_id = {str(project_id)};"""
            cursor.execute(query)
            
            self.db_manager.get_conn().commit()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_delete_project : {e}")
            self.db_manager.get_conn().rollback()
            return ERROR
        

    def API_alert_project(self, user_id, project_id, project_name, project_description, team, todo, appointment):
        try :
            # 유효성 검사 user_id project leader인지 확인 - 다른 사람이 삭제했을 수도 있음
            query = f"""SELECT * FROM project WHERE project_leader = '{user_id}' AND project_id = {str(project_id)};"""
            cursor = self.db_manager.get_cursor()
            cursor.execute(query)
            result = cursor.fetchone() # Primary Key
            if not result:
                return ERROR

            query = f"""UPDATE project SET project_name = {project_name}, 
            project_description = {project_description}  
            WHERE project_id = {str(project_id)};
            """
            cursor.execute(query)

            query = f"""DELETE FROM project_belong WHERE project_id = {str(project_id)};"""
            cursor.execute(query)

            for team_id in team:
                query = f"""INSERT INTO project_belong(project_id, user_id) VALUES({str(project_id)}, '{team_id}');"""
                cursor.execute(query)

            self.db_manager.get_conn().commit()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_delete_project : {e}")
            self.db_manager.get_conn().rollback()
            return ERROR
        