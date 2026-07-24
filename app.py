# app.py
from flask import Flask, jsonify, request, render_template
from storage import Storage
from models import Task

app = Flask(__name__)
storage = Storage()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = storage.load_tasks()
    return jsonify([task.to_dict() for task in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    description = data.get("description", "").strip()
    due_date = data.get("due_date")
    assigned_to = data.get("assigned_to")

    tasks = storage.load_tasks()
    new_id = max([t.id for t in tasks], default=0) + 1
    task = Task.create_new(new_id, title, description, due_date, assigned_to)
    tasks.append(task)
    storage.save_tasks(tasks)

    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    tasks = storage.load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            storage.save_tasks(tasks)
            return jsonify(task.to_dict())
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = storage.load_tasks()
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            storage.save_tasks(tasks)
            return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)