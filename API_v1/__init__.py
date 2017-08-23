import api


from flask import Blueprint


blueprint = Blueprint('1.0', __name__)

# Routing
blueprint.add_url_rule('/api/login', 'login', api.login, methods=['POST'])
#blueprint.add_url_rule('/api/pwd_hash', 'pwd_hash', api.pwd_hash, methods=['GET'])
#blueprint.add_url_rule('/api/director', 'director', api.director, methods=['GET'])
blueprint.add_url_rule('/api/director_info', 'director_info', api.director_info, methods=['GET'])
blueprint.add_url_rule('/api/company_by_director', 'company_by_director', api.company_by_director, methods=['GET'])
blueprint.add_url_rule('/api/director_by_company', 'director_by_company', api.director_by_company, methods=['GET'])
blueprint.add_url_rule('/api/get_news', 'get_news', api.get_news, methods=['GET'])