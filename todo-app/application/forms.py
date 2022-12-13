from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import date

class IsFutureDate():
    def __init__(self, message = "Date should be in the future!"):
        self.message = message
    
    def __call__(self, form, field):
        if field.data < date.today():
            raise ValidationError(message = self.message)
        return True

class CreateTask(FlaskForm):
    name = StringField("Task Name", validators=[DataRequired()])
    desc = StringField("Task Description", validators=[DataRequired()])
    priority = IntegerField("Priority Level", validators=[DataRequired(), NumberRange(1, 5)])
    due = DateField("Due Date", validators=[DataRequired(), IsFutureDate()])
    user = SelectField("Assignee", choices=[], validators=[DataRequired()])
    submit = SubmitField("Add Task")

class CreateUser(FlaskForm):
    forename = StringField("Forename", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    submit = SubmitField("Add User")