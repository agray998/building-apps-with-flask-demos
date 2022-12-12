from application import app, db
from flask import request
from application.models import Tasks

@app.route("/")
def index():
    return "Todo List!"

@app.route("/add")
def add_todo():
    name = request.args.get("name")
    desc = request.args.get("desc")
    priority = int(request.args.get("priority"))
    due = request.args.get("due")
    task = Tasks(name=name, description=desc, priority=priority, due=due)
    db.session.add(task)
    db.session.commit()
    return f"Added {str(task)}"

