from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import init_app as init_db
from app.routes.users import bp as users_bp
from app.routes.expenses import bp as expenses_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    JWTManager(app)
    init_db(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(expenses_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
