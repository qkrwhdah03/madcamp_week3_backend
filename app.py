from flask import Flask, request
from flask_cors import CORS
from util.DBmanager import DBmanager
from util.APImanager import APImanager

########## MYSQL DB Connection Variables ######
HOST = "localhost"
PORT = 3306
DBNAME = "week3"
USER = "week3_user"
PASSWORD = "madcamp"
###############################################

########## CODE for fail validity information #
CODE = "NOT VALID"
###############################################

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False # 한글깨짐 방지


##################################################

#   API 

##################################################

# Main
@app.route("/")
def main():
    return "Connection Done"

# User 확인 API
@app.route("/user", methods=['GET'])
def user():
    user_id = request.args.get('user_id')
    return api.API_check_user(user_id)

# Login 처리 API
@app.route("/login", methods=['GET'])
def login():
    user_id = request.args.get('user_id')
    password = request.args.get('user_pw')
    #print(user_id, password)
    return api.API_login(user_id, password)

# 아이디 중복 확인 API
@app.route("/duplicate", methods=['GET'])
def duplicate():
    user_id = request.args.get('user_id')
    return api.API_duplicate(user_id)


# Register 처리 API
@app.route("/register", methods=['POST']) 
def register():
    # POST 결과 얻어오기
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')
    password_check = data.get('password_check')
    name = data.get('name')
    belong = data.get('belong')
    #print(user_id, password, name, belong)

    # 유효성 검사
    # 1. 비밀번호 일치 여부 
    # 2. user_id 길이 1~15자 이하
    # 3. password는 hash 값이라 256이하임.
    # 4. name 길이 1~10
    # 5. belong 길이 1~25
    
    if password != password_check:
        return CODE
    elif not (1<= len(user_id) <= 15):
        return CODE
    elif not (1<= len(name) <= 10):
        return CODE
    elif not (1<= len(belong) <= 25):
        return CODE

    return api.API_register(user_id, password, name, belong)

# 로그인 후, Profile 가져오는 API
@app.route("/profile", methods=['GET'])
def profile():
    user_id = request.args.get('user_id')
    #print(user_id)
    return api.API_get_profile(user_id)


@app.route("/create_project", methods=['POST'])
def create_project():
    data = request.json
    title = data.get('name')
    description = data.get('description')
    team = data.get('team')
    leader = data.get('leader')

    # 유효성 검사 + 프론트도 조건 추가 필요
    if not(1<= len(title) <= 15): # 프로젝트 이름은 15자이하
        return CODE
    if not(0<= len(description) <= 50): # 프로젝트 설명 50자이하
        return CODE
    if not(1<= len(team)): # 팀원은 최소 한 명
        return CODE
    
    return api.API_register_project(title, leader, description, team)


@app.route("/delete_project", methods=['POST'])
def delete_project():
    data = request.json
    project_id = data.get('project_id')
    return api.API_delete_project(project_id)

@app.route("/alert_project", methods = ['POST'])
def alert_project():
    data = request.json
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    project_name = data.get('project_name')
    project_description = data.get('description')
    team = data.get('participants').split(',')
    todo = data.get('todo') 
    appointment = data.get('appointment')
    #print(data)
    #print(team)
    return api.API_alert_project(user_id, project_id, project_name, project_description, team, todo, appointment)



if __name__ == "__main__":
    db_manager = DBmanager(HOST, USER, PORT, PASSWORD, DBNAME)
    api = APImanager(db_manager)
    app.run(host="0.0.0.0", port = 80) # Server 실행