from application import app, db

class Tasks(db.Model): # tasks table
    # __tablename__ = "todo_items" - if changing table name
    # need: due date, priority level, name, description
    task_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    due = db.Column(db.String(10))
    def __str__(self):
        return f"{self.name}: {self.description}, due {self.due}. Priority {self.priority}."