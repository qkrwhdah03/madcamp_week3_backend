from flask import Flask
from util.DBmanager import DBmanager
from util.APImanager import APImanager

########## MYSQL DB Connection Variables ######
HOST = "localhost"
PORT = 3306
DBNAME = "week3"
USER = "week3_user"
PASSWORD = "madcamp"
###############################################


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 한글깨짐 방지



##################################################

#   API 

##################################################

# Main
@app.route("/")
def main():
    return "Connection Done"

# Login 처리 API
@app.route("/login/<user_id>/<password>", methods=['GET'])
def login(user_id, password):
    return api.API_login(user_id, password)

# Register 처리 API
@app.route("/register/<user_id>/<password>/<name>/<belong>", methods=['GET']) 
def register(user_id, password, name, belong):
    return api.API_register(user_id, password, name, belong)

# 로그인 후, Profile 가져오는 API
@app.route("/profile/<user_id>", methods=['GET'])
def profile(user_id):
    return api.API_get_profile(user_id)


if __name__ == "__main__":
    db_manager = DBmanager(HOST, USER, PORT, PASSWORD, DBNAME)
    api = APImanager(db_manager)
    app.run(host="0.0.0.0", port = 80) # Server 실행