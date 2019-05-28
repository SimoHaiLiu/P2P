from flask import Flask
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/qupital'
app.config['SECRET_KEY'] = 'Ay98Cct2oNSlnHDdTl8'

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'wmltyq@qq.com'
app.config['MAIL_PASSWORD'] = 'cfafqtnudfoydhcb'
mail = Mail(app)

mongo = PyMongo(app)
db = SQLAlchemy()
db.init_app(app)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
# 指定了未登录时跳转的页面
login_manager.login_view = 'login'
login_manager.init_app(app)

topbar = Navbar('Qupital',
                View('Home', 'index'),
                View('Params', 'params'),
                # Subgroup('Auctions',
                #          View('Current Auctions', 'index', auctions_tyoe='auction'),
                #          View('Past Auctions', 'index', auctions_type='current_auctions'))
                )
nav = Nav()
nav.register_element('top', topbar)
nav.init_app(app)

csrf = CsrfProtect()
csrf.init_app(app)
