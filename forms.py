from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    userName = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    rememberMe = BooleanField('记住我？')
    submit = SubmitField('登录')


class PostForm(Form):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('发布')
