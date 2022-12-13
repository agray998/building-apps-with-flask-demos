from application import app, db
from flask import request, redirect, url_for, render_template
from application.models import Tasks, Users
from application.forms import CreateTask

@app.route("/")
def index():
    return render_template('index.html')

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
    return redirect(url_for('view_users'))

@app.route("/view-users")
def view_users():
    users = Users.query.all()
    return render_template('view-users.html', users = users)

@app.route("/update-user/<int:id>")
def update_user(id):
    user = Users.query.get(id)
    user.forename = request.args.get("forename", user.forename)
    user.surname = request.args.get("surname", user.surname)
    db.session.commit()
    return redirect(url_for('view_users'))

@app.route("/delete-user/<int:id>")
def delete_user(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('view_users'))

@app.route("/add", methods=["GET", "POST"])
def add_todo():
    form = CreateTask()
    form.user.choices = [(user.user_id, f"{user.forename} {user.surname}") for user in Users.query.all()]
    if form.validate_on_submit():
        user = form.user.data
        name = form.name.data
        desc = form.desc.data
        priority = form.priority.data
        due = form.due.data
        task = Tasks(name=name, description=desc, priority=priority, due=due, user = user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('view_tasks'))
    return render_template('add-task.html', form = form, heading="Add Task")

@app.route("/view-tasks")
def view_tasks():
    tasks = Tasks.query.order_by(Tasks.priority).all() # can user filter_by to narrow results, eg: Tasks.query.filter_by(name="sample 2").all()
    return render_template('view-tasks.html', tasks=tasks)

@app.route("/task/<int:id>")
def get_task(id):
    return str(Tasks.query.get(id))

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update_task(id):
    task = Tasks.query.get(id)
    form = CreateTask() # creating new form object
    form.submit.label.text = "Update Task" # changing text on update button - useful when re-using forms
    form.user.choices = [(user.user_id, f"{user.forename} {user.surname}") for user in Users.query.all()] # dynamically populating select field with data from database
    if form.validate_on_submit(): # checking whether form has been submitted, and meets all validation requirements
        task.name = form.name.data
        task.description = form.desc.data
        task.priority = form.priority.data
        task.due = form.due.data
        task.user = form.user.data
        db.session.commit()
        return redirect(url_for('view_tasks'))
    # pre-populating the update form with existing data - convenient for end user
    form.name.data = task.name
    form.desc.data = task.description
    form.priority.data = task.priority
    form.due.data = task.due
    form.user.data = task.user
    return render_template('add-task.html', form=form, heading="Update Task")

@app.route("/delete-task/<int:id>")
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))