from flask import Flask
from flask_cors import CORS, cross_origin
# from blueprints.basic_endpoints import blueprint as basic_endpoints
# from blueprints.documented_endpoints import blueprint as documented_endpoint


app = Flask(__name__)
# app.config['RESTPLUS_MASK_SWAGGER'] = False
# app.register_blueprint(basic_endpoints)
# app.register_blueprint(documented_endpoint)
CORS(app)