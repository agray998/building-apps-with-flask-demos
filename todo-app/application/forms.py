from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField

class CreateTask(FlaskForm):
    name = StringField("Task Name")
    desc = StringField("Task Description")
    priority = IntegerField("Priority Level")
    due = DateField("Due Date")
    user = SelectField("Assignee", choices=[])
    submit = SubmitField("Add Task")