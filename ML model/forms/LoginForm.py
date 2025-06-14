from flask_wtf import FlaskForm
from wtforms import (StringField ,SelectField ,DateField ,PasswordField ,BooleanField ,SubmitField
    
)
from wtforms.validators import (DataRequired ,Length  ,Email  ,Optional ,EqualTo)

class SignForm(FlaskForm):
    username= StringField("Username",
    validators =[DataRequired() ,Length(2,30)]   # validation i.e required 
    )
    email =StringField("Email" ,
    validators =[DataRequired() , Email()]
    )
    gender =SelectField( "Gender" ,
        choices=['Male','Female','Other'] ,
        validators=[Optional()]
    )
    dob = DateField(
        " Date of Birth" ,
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password"
        ,validators=[DataRequired(),Length(5,25)]
    )
    confirm_password = PasswordField(
        "Confirm Password"
        ,validators=[DataRequired(),Length(5,25) ,EqualTo('password')]
    )
    submit =SubmitField("Signup")  

class LoginForm(FlaskForm):
    email =StringField("Email" ,
    validators =[DataRequired() , Email()]
    )
    password = PasswordField(
        "Password"
        ,validators=[DataRequired(),Length(5,25)] )
    remember_me =BooleanField("remember me" )
    submit =SubmitField("Login")
