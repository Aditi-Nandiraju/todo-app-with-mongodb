
import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

# Task 1: uses local MongoDB by default.
# Task 2: on Render, set the MONGO_URI environment variable to your Atlas connection string.
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["beginner_db"]
todos_collection = db["todos"]


@app.route("/")
def index():
    # Fetch all documents from the NoSQL collection
    all_todos = list(todos_collection.find())
    return render_template("index.html", todos=all_todos)


@app.route("/add", methods=["POST"])
def add_todo():
    task = request.form.get("task")
    if task:
        # Insert a JSON-like document into MongoDB
        todos_collection.insert_one({"task": task, "done": False})
    return redirect("/")


@app.route("/toggle/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    try:
        oid = ObjectId(todo_id)
    except InvalidId:
        return redirect("/")
    todo = todos_collection.find_one({"_id": oid})
    if todo:
        todos_collection.update_one(
            {"_id": oid}, {"$set": {"done": not todo.get("done", False)}}
        )
    return redirect("/")


@app.route("/delete/<todo_id>", methods=["POST"])
def delete_todo(todo_id):
    try:
        todos_collection.delete_one({"_id": ObjectId(todo_id)})
    except InvalidId:
        pass
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
