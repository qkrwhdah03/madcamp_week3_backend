import json

class JSONconverter :
    def __init__(self,): 
        return
    
    def convert_profile_info(self, user_info, project_list, team_list, todo_list, appointment_list, schedule_list):
        json_dict = {}
        # User info
        json_dict['user_id'] = user_info[0]
        json_dict['user_name'] = user_info[2]
        json_dict['user_belong'] = user_info[3]

        # Project
        project_converted_list = []
        for project, team, todo, appointment in zip(project_list, team_list, todo_list, appointment_list):
            project_dict = {}
            
            project_dict['project_id'] = int(project[0])
            project_dict['project_name'] = project[1]
            project_dict['project_description'] = project[2]
            project_dict['project_leader'] = project[3]
            project_dict['team'] = team

            # Todo
            todo_converted_list = []
            for todo_item in todo:
                todo_dict = {}
                todo_dict['text'] = todo_item[2]
                todo_dict['isChecked'] = True if todo_item[3]=="True" else False
                todo_converted_list.append(todo_dict)

            project_dict['todo'] = todo_converted_list
            
            #appointment
            app_converted_list = []
            for appointment_item in appointment:
                app_dict = {}
                app_dict['text'] = appointment_item[2]
                app_dict['isChecked'] = True if appointment_item[3]=="True" else False
                app_converted_list.append(app_dict)

            project_dict['appointment'] = app_converted_list
            project_converted_list.append(project_dict)
        

        json_dict['project'] = project_converted_list   

        schedule_converted_list = []
        for item in schedule_list:
            dic = {}
            dic['plan_name'] = item[2] # schedule_info
            dic['left_index'] = int(item[3]) # dayofweek
            dic['top_index'] = int(item[4]) # start_time
            dic['plan_time'] = int(item[5]) # length
            schedule_converted_list.append(dic)
        
        json_dict['schedule'] = schedule_converted_list
        return json.dumps(json_dict, ensure_ascii=False)
    
    def convert_user_search_result(self, search_list):
        return json.dumps({'result':search_list}, ensure_ascii=False)
    
    def convert_gather_schedule(self, gather, person):
        return json.dumps({'gathered_schedule': gather, 'who':person}, ensure_ascii=False)
    
    def convert_project_info(self, project, team, todo, appointment, schedule_list):
        json_dict = {}
        project_dict = {}
            
        project_dict['project_id'] = int(project[0])
        project_dict['project_name'] = project[1]
        project_dict['project_description'] = project[2]
        project_dict['project_leader'] = project[3]
        project_dict['team'] = team

        # Todo
        todo_converted_list = []
        for todo_item in todo:
            todo_dict = {}
            todo_dict['text'] = todo_item[2]
            todo_dict['isChecked'] = True if todo_item[3]=="True" else False
            todo_converted_list.append(todo_dict)

        project_dict['todo'] = todo_converted_list
        
        #appointment
        app_converted_list = []
        for appointment_item in appointment:
            app_dict = {}
            app_dict['text'] = appointment_item[2]
            app_dict['isChecked'] = True if appointment_item[3]=="True" else False
            app_converted_list.append(app_dict)

        project_dict['appointment'] = app_converted_list
        
        json_dict['project'] = project_dict

        schedule_converted_list = []
        for item in schedule_list:
            dic = {}
            dic['plan_name'] = item[2] # schedule_info
            dic['left_index'] = int(item[3]) # dayofweek
            dic['top_index'] = int(item[4]) # start_time
            dic['plan_time'] = int(item[5]) # length
            schedule_converted_list.append(dic)

        json_dict['schedule'] = schedule_converted_list
        print(json.dumps(json_dict, ensure_ascii=False))
        return json.dumps(json_dict, ensure_ascii=False)

