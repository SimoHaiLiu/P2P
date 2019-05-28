from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from models import *


class Params(FlaskForm):
    advanced_amount = FloatField('Advanced Amount', validators=[DataRequired(message='Not Null')])
    account_receivable = FloatField('Account Receivable(1000000~100000000)', validators=[DataRequired(message='Not Null')])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(1, 64), Email])
    username = StringField(label='用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField(label='密码', validators=[DataRequired(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField(label='确认密码', validators=[DataRequired()])
    submit = SubmitField(label='注册')

    def generate_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    # 自定义用户名验证器
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已注册，请选用其它名称')

    # 自定义邮箱验证器
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册，请选用其它邮箱')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default=False)
    submit = SubmitField('登录')
