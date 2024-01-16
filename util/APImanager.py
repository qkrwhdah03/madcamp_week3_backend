from util.JSONconverter import JSONconverter
import traceback

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
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            search_query = f"""SELECT * FROM user WHERE user_id = '{user_id}'; """
            cursor = conn.cursor()
            cursor.execute(search_query)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                return TRUE
            else :
                return FALSE
            
        except Exception as e:
            print(f"Error in API_check_user : {e}")
            traceback.print_exc()
            return ERROR

    def API_login(self, user_id, password):
        # 로그인 정보가 있는지 확인해서 확인 코드 반환
        try :
            search_query = f"""
                SELECT * 
                FROM user
                WHERE user_id = '{user_id}' AND password = '{password}';
            """
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(search_query)
            result = cursor.fetchone() # WE have to ensure that there is unique user_id..
            cursor.close()
            conn.close()
            if result:
                return TRUE
            else :
                return FALSE
            
        except Exception as e :
            print(f"Error in API_login : {e}")
            traceback.print_exc()
            return ERROR
    
    def API_duplicate(self, user_id):
        try :
            duplicate_request = f"""SELECT * FROM user WHERE user_id ='{user_id}';"""
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(duplicate_request)
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                return FALSE
            else :
                return TRUE
            
        except Exception as e:
            print(f"Error in API_duplicate : {e}")
            traceback.print_exc()
            return ERROR


    def API_register(self, user_id, password, name, belong):
        try :
            save_register_query = f"""INSERT INTO user(user_id, password, name, belong) 
            VALUES('{user_id}', '{password}', '{name}', '{belong}')
            """
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(save_register_query)

            conn.commit()
            cursor.close()
            conn.close()

            return TRUE
        except Exception as e:
            print(f"Error in API_register : {e}")
            traceback.print_exc()
            conn.rollback()
            return ERROR
        
    def API_get_profile(self, user_id):
        # User Table
        try : 
            get_profile_query = f"""SELECT * FROM user WHERE user_id = '{user_id}';"""
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(get_profile_query)
            user_info_result = cursor.fetchone()

            if not user_info_result:
                print("Error in API_get_profile no such value")
                return ERROR
        
            # Get Project id
            get_project_list_query = f"""SELECT * FROM project_belong WHERE user_id = '{user_id}';"""

            cursor.execute(get_project_list_query)
            result = cursor.fetchall() # 한 명이 여러 개의 프로젝트도 가능
            
            project_list = []
            teammate_list = []
            todo_list = []
            appointment_list = []
            
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

                # Get Project Todo
                get_project_todo_query =f"""SELECT * FROM todo WHERE project_id = '{str(project_id)}';"""
                cursor.execute(get_project_todo_query)
                todos = cursor.fetchall()

                todo = []
                for todo_item in todos :
                    todo.append(todo_item)
                todo_list.append(todo)

                # Get Project Appointment
                get_project_appointment_query =f"""SELECT * FROM appointment WHERE project_id = '{str(project_id)}';"""
                cursor.execute(get_project_appointment_query)
                apps = cursor.fetchall()

                appointments = []
                for apps_item in apps:
                    appointments.append(apps_item)
                appointment_list.append(appointments)


            # Get Project Schedule
            query = f"""SELECT * FROM schedule WHERE user_id = '{user_id}';"""
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            schedule_list = []
            for item in result:
                schedule_list.append(item)
                

            return self.convert.convert_profile_info(user_info_result, project_list, teammate_list, todo_list, appointment_list, schedule_list)

        except Exception as e:
            print(f"Error in API_get_Profile : {e}")
            traceback.print_exc()
            return ERROR   
        
    def API_register_project(self, name, leader, description, team_list): # Project Leader 추가하기 - 받아와야함
        try :
            query = f"""INSERT INTO project(project_name, project_description, project_leader) VALUES('{name}', '{description}','{leader}');"""
            
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(query)
            
            project_id = cursor.lastrowid 
            
            if project_id == None:
                raise Exception("Fail to get project_id")

            # project_belong Table에 team_list 추가
            for team in team_list:
                query = f"""INSERT INTO project_belong(project_id, user_id) VALUES({str(project_id)},'{team}');"""
                cursor.execute(query)

            conn.commit()
            cursor.close()
            conn.close()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_register-project : {e}")
            traceback.print_exc()
            conn.rollback()
            return ERROR
        
    def API_delete_project(self, project_id):
        try :
            query = f"""DELETE FROM project_belong WHERE project_id = {str(project_id)};"""
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            cursor.execute(query)

            query = f"""DELETE FROM project WHERE project_id = {str(project_id)};"""
            cursor.execute(query)
            
            conn.commit()
            cursor.close()
            conn.close()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_delete_project : {e}")
            traceback.print_exc()
            conn.rollback()
            return ERROR
        

    def API_alert_project(self, user_id, project_id, project_name, project_description, team, todo, appointment):
        try :
            # 유효성 검사 user_id project leader인지 확인 - 다른 사람이 삭제했을 수도 있음
            #query = f"""SELECT * FROM project WHERE project_leader = '{user_id}' AND project_id = {str(project_id)};"""
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            #cursor.execute(query)
            #result = cursor.fetchone() # Primary Key
            #if not result:
            #    return ERROR
            # Project Table 업데이트
            query = f"""UPDATE project SET project_name = '{project_name}', 
            project_description = '{project_description}'  
            WHERE project_id = {str(project_id)};
            """
            cursor.execute(query)

            # Proejct_belong table 업데이트
            query = f"""DELETE FROM project_belong WHERE project_id = {str(project_id)};"""
            cursor.execute(query)

            for team_id in team:
                query = f"""INSERT INTO project_belong(project_id, user_id) VALUES({str(project_id)}, '{team_id}');"""
                cursor.execute(query)

            #Todo Table
            query = f"""DELETE FROM todo WHERE project_id = {str(project_id)}"""
            cursor.execute(query)

            #print(todo)
            for todo_item in todo:
                #todo_item = dict(todo_item)
                print(todo_item, type(todo_item))
                todo_text = todo_item['text']
                todo_check = todo_item['isChecked']
                #print(todo_check, type(todo_check))
                query = f"""INSERT INTO todo(project_id, todo, todo_check) 
                            VALUES({str(project_id)},'{todo_text}','{todo_check}');"""
                cursor.execute(query)

            #Appointment Table
            query = f"""DELETE FROM appointment WHERE project_id = {str(project_id)};"""
            cursor.execute(query)

            for app_item in appointment:
                app_item = dict(app_item)
             
                app_text = app_item['text']
                app_check = app_item['isChecked']
                query = f"""INSERT INTO appointment(project_id, appointment, appointment_check) VALUES({str(project_id)},'{app_text}','{app_check}');"""
                cursor.execute(query)

            conn.commit()
            cursor.close()
            conn.close()
            return TRUE
        
        except Exception as e:
            print(f"Error in API_alert_project : {e}")
            traceback.print_exc()
            conn.rollback()
            return ERROR
        
    def API_set_schedule(self, user_id, schedule_list):
        try:

            # user_id의 스케줄을 초기화
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            query = f"""DELETE FROM schedule WHERE user_id = '{user_id}';"""

            cursor.execute(query)

            for schedule in schedule_list:
                user_id = schedule['user_id']
                schedule_info = schedule['schedule_info']
                dayofweek = schedule['dayofweek']
                start_time = schedule['start_time']
                length = schedule['length']

                query = f"""INSERT INTO schedule(user_id, schedule_info, dayofweek, start_time, length)
                    VALUES('{user_id}','{schedule_info}',{str(dayofweek)},{str(start_time)},{str(length)});"""
                cursor.execute(query)

            conn.commit()
            cursor.close()
            conn.close()

            return TRUE
        except Exception as e:
            conn.rollback()
            print(f"Error in API_set_schedule : {e}")
            traceback.print_exc()
            return ERROR
        
    def API_gather_schedule(self, team):
        try :
            gather = [[0 for i in range(7)] for j in range(24)]
            person = [[[] for i in range(7)] for j in range(24)]
            result_list = []
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()
            for user in team:

                query = f"""SELECT * FROM schedule WHERE user_id = '{user}';"""
                cursor.execute(query)
                result = cursor.fetchall()
                result_list.extend(result)
                
            conn.close()

            for schedule in result_list:
                id = schedule[1] # user_id
                x = schedule[4] # start_time
                y = schedule[3] # dayofweek
                t = schedule[5] # lenght
                i = 0
                while i<t:
                    gather[x+i][y] += 1
                    person[x+i][y].append(id)
                    i+=1

            return self.convert.convert_gather_schedule(gather, person)

        except Exception as e :
            print(f"Error in API_gather_schedule : {e}")
            traceback.print_exc()
            return ERROR
        
    def API_get_project_info(self, user_id, project_id):
        try:
            conn = self.db_manager.get_conn()
            cursor = conn.cursor()

            get_project_info_query = f"""SELECT * FROM project WHERE project_id = {str(project_id)};"""
            cursor.execute(get_project_info_query)
            project = cursor.fetchone()  # project_id is PK
                
            # Get Project Team
            get_project_team_query =f"""SELECT * FROM project_belong WHERE project_id = '{str(project_id)}';"""
            cursor.execute(get_project_team_query)
            team = cursor.fetchall() # 팀은 여러 명 가능
            #print(team)
            teammate = []
            for team_user in team:
                teammate.append(team_user[1])  # project_belong의 user_id index

            # Get Project Todo
            get_project_todo_query =f"""SELECT * FROM todo WHERE project_id = '{str(project_id)}';"""
            cursor.execute(get_project_todo_query)
            todos = cursor.fetchall()

            todo = []
            for todo_item in todos :
                todo.append(todo_item)

            # Get Project Appointment
            get_project_appointment_query =f"""SELECT * FROM appointment WHERE project_id = '{str(project_id)}';"""
            cursor.execute(get_project_appointment_query)
            apps = cursor.fetchall()

            appointments = []
            for apps_item in apps:
                appointments.append(apps_item)


            # Get Schedule
            query = f"""SELECT * FROM schedule WHERE user_id = '{user_id}';"""
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            schedule_list = []
            for item in result:
                schedule_list.append(item)


            cursor.close()
            conn.close()

            return self.convert.convert_project_info(project, teammate, todo, appointments, schedule_list)

        except Exception as e : 
            print(f"Error in API_get_project_info : {e}")
            traceback.print_exc()
            return ERROR
