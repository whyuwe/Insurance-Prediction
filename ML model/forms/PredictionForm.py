# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    submit = SubmitField("Login")

class PredictionForm(FlaskForm):
    age = IntegerField("Age", validators=[
        DataRequired(), NumberRange(min=1, max=120, message="Enter valid age between 1 and 120")
    ])
    
    weight = FloatField("Weight (kg)", validators=[
        DataRequired(), NumberRange(min=1, message="Weight must be greater than 0")
    ])
    
    height = FloatField("Height (m)", validators=[
        DataRequired(), NumberRange(min=0.5, max=2.5, message="Height must be between 0.5 and 2.5 meters")
    ])
    
    income_lpa = FloatField("Annual Income (LPA)", validators=[
        DataRequired(), NumberRange(min=0, message="Income must be non-negative")
    ])
    
    smoker = SelectField(
        "Do you Smoke?",
        choices=[(True, "Yes"), (False, "No")],
        coerce=lambda x: x == "True",
        validators=[DataRequired()]
    )

    city = StringField("City", validators=[
        DataRequired(), Length(min=2, message="Enter a valid city name")
    ])
    
    occupation = SelectField(
        "Occupation",
        choices=[
            ('retired', 'Retired'),
            ('freelancer', 'Freelancer'),
            ('student', 'Student'),
            ('government_job', 'Government Job'),
            ('bussiness_owner', 'Business Owner'),
            ('unemployed', 'Unemployed'),
            ('private_job', 'Private Job')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Predict")
