from application import app, db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    forename = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    tasks = db.relationship('Tasks', backref="users") # user.tasks holds list of tasks associated to user, also creates backref to access a user from their tasks

class Tasks(db.Model): # tasks table
    # __tablename__ = "todo_items" - if changing table name
    # need: due date, priority level, name, description
    task_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    due = db.Column(db.String(10))
    user = db.Column(db.Integer, db.ForeignKey('users.user_id')) # creates foreign key constraint
    def __str__(self):
        return f"{self.name}: {self.description}, due {self.due}. Priority {self.priority}. Assignee: {self.users.forename} {self.users.surname}"
