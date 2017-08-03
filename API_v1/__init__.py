import users


from flask import Blueprint


blueprint = Blueprint('1.0', __name__)

# API Routing
blueprint.add_url_rule('/user/login', 'login', users.login, methods=['POST'])
blueprint.add_url_rule('/user/pwd_hash', 'pwd_hash', users.pwd_hash, methods=['GET'])