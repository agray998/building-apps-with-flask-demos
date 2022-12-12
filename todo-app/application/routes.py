from application import app, db
from flask import request, redirect, url_for
from application.models import Tasks, Users

@app.route("/")
def index():
    return "Todo List!"

# DB operations
# (c)reate /
# (r)ead /
# (u)pdate /
# (d)elete /

@app.route("/add-user")
def add_user():
    forename, surname = request.args.get("forename"), request.args.get("surname")
    user = Users(forename = forename, surname = surname)
    db.session.add(user)
    db.session.commit()
    return "added user"

@app.route("/add")
def add_todo():
    user = int(request.args.get("user"))
    name = request.args.get("name")
    desc = request.args.get("desc")
    priority = int(request.args.get("priority"))
    due = request.args.get("due")
    task = Tasks(name=name, description=desc, priority=priority, due=due, user = user)
    db.session.add(task)
    db.session.commit()
    return f"Added {str(task)}"

@app.route("/view-tasks")
def view_tasks():
    tasks = Tasks.query.order_by(Tasks.priority).all() # can user filter_by to narrow results, eg: filter_by(name="sample 2")
    return '<br>'.join(map(str, tasks))

@app.route("/task/<int:id>")
def get_task(id):
    return str(Tasks.query.get(id))

@app.route("/update/<int:id>")
def update_task(id):
    task = Tasks.query.get(id)
    task.name = request.args.get("name", task.name)
    task.description = request.args.get("desc", task.description)
    task.priority = int(request.args.get("priority", task.priority))
    task.due = request.args.get("due", task.due)
    task.user = int(request.args.get("user", task.user))
    db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route("/delete-task/<int:id>")
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))