from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class UploadForm(FlaskForm):
    file = FileField(
        'Upload Image',
        validators=[
            FileRequired(message="File cannot be empty."),
            FileAllowed(['jpg', 'jpeg', 'png'], message="Only images are allowed.")
        ]
    )