from flask import Flask
from admin.models import db
from datetime import timedelta
from admin.app import app
from settings.settings import third
from channels.channel import fourth

second = Flask(__name__)
second.secret_key = "lovely29"
second.permanent_session_lifetime = timedelta(days=1)
second.app_context().push()

second.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
second.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(second)

second.register_blueprint(app, url_prefix='/admin')
second.register_blueprint(third, url_prefix='/admin/settings')
second.register_blueprint(fourth, url_prefix='/admin/channels')


if __name__ == "__main__":
    db.create_all()
    second.run(debug=True, port=8000)