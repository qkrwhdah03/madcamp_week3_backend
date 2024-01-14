import json

class JSONconverter :
    def __init__(self,): 
        return
    
    def convert_profile_info(self, user_info, project_list, team_list):
        json_dict = {}
        # User info
        json_dict['user_id'] = user_info[0]
        json_dict['user_name'] = user_info[2]
        json_dict['user_belong'] = user_info[3]

        # Project
        project_converted_list = []
        for project, team in zip(project_list, team_list):
            project_dict = {}
            
            project_dict['project_id'] = project[0]
            project_dict['project_name'] = project[1]
            project_dict['project_description'] = project[2]
            project_dict['project_leader'] = project[3]
            project_dict['team'] = team

            project_converted_list.append(project_dict)

        json_dict['project'] = project_converted_list

        return json.dumps(json_dict, ensure_ascii=False)
    
    def convert_user_search_result(self, search_list):
        return json.dumps({'result':search_list}, ensure_ascii=False)