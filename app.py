from flask import Flask, request

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index(): # view function
    return "Hello World!", 201

@app.route("/greet/<name>", methods = ["GET", "POST", "PUT"])
def greet(name):
    return f"Hello, {name}, you made a {request.method} request"

@app.route("/number/<int:num>")
def square(num):
    return {"number": num, "number squared": num ** 2}

if __name__ == '__main__':
    app.run(debug = True)