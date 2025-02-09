from flask_wtf import ( FlaskForm )
from wtforms import ( StringField )
from wtforms.validators import ( DataRequired, InputRequired )

class AdminLoginForm(FlaskForm):
    '''
    Form controlling login into the admin section of the site
    '''
    name = StringField(
        'Username',
        validators=[
            DataRequired("A username value must be provided"),
            InputRequired("Username and password fields can not be empty!")
        ],
    )
    password = StringField(
        'Password',
        validators=[
            DataRequired(message="A password value is required."),
            InputRequired("Username and password fields can not be empty!")
        ]
    )