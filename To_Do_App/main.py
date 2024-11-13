import json
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

def get_task_id(id_filter):
    with open("data.json", "r") as file:
        tasks_with_id= json.load(file)
    return next((task for task in tasks_with_id['tasks'] if task.get("id")==id_filter), None)

@app.route("/")
def index():
    with open("data.json", "r") as file:
       all_tasks_data = json.load(file)

    return render_template('tasks.html', tasks=all_tasks_data['tasks'])

def add_task_index():
    add = add_task()

    return render_template('task.html', add = add_task['tasks'])

@app.route("/tasks")
def get_all_tasks():
    with open("data.json", "r") as file:
       all_tasks_data = json.load(file)

    status_filter = request.args.get('status', default = None, type = str)
    if status_filter:
        filtred_tasks = [task for task in all_tasks_data["tasks"] if task.get('status') == status_filter]
        return jsonify({"tasks": filtred_tasks})

    return jsonify(all_tasks_data)

@app.route("/task_id")
def get_id():
    id_filter = request.args.get("id", type=int)
    task = get_task_id(id_filter)

    if task is None:
        return {"error": "Task not found"}, 404
    else:
        return jsonify(task)


@app.route("/tasks", methods=["POST"])
def add_task():
    request_data=request.json
    id = request_data.get("id")
    description = request_data.get("description")
    category = request_data.get("category")
    status = request_data.get("status", "pending")

    if not id:
         return {"error":"id is required"}, 400
    try:
         with open("data.json", "r") as file:
          all_tasks_data = json.load(file)

    except FileNotFoundError:
        all_tasks_data = {"tasks":[]}

    if any(task.get("id") == id for task in all_tasks_data["tasks"]):
           return {"error": "Id is not unique"}, 400

    new_task = {
           "id": id,
           "description" : description,
           "category" :category,
           "status": status
       }

    all_tasks_data["tasks"].append(new_task)

    with open("data.json", 'w') as file:
        json.dump(all_tasks_data, file, indent=4)

    return {
        'message':f"Task with {id}, description {description}, category {category} and status {status} added successfully!"
    }

@app.route('/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id):

    with (open("data.json", "r") as file):
         new_data = json.load(file)

    tasks_before_delete = len(new_data["tasks"])

    new_data['tasks']=[task for task in new_data["tasks"] if task['id'] != task_id]
    if len(new_data['tasks']) == tasks_before_delete:
          return {"error": "Task not found"}, 404

    with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)

    return {"message": f"Task with ID {task_id} deleted successfully!"}, 200


@app.route("/tasks", methods=["PUT"])
def update_tasks():
    id_filter = request.args.get("id", type=int)

    update = get_task_id(id_filter)
    if update is None:
        return {"error":"Task not found"},404

    request_data = request.json
    id = request_data.get("id", update["id"])
    description = request_data.get("description", update["description"])
    category = request_data.get("category", update["category"])
    status = request_data.get("status",update["status"])

    update["id"]= id
    update["description"] = description
    update["category"] = category
    update["status"] = status

    with open("data.json", 'r') as file:
        all_tasks_data = json.load(file)

        for task in all_tasks_data["tasks"]:
            if task["id"] == id_filter:
                task.update(update)

        with open("data.json", "w") as file:
            json.dump(all_tasks_data, file, indent=4)

    return {
        'message': f"Task with ID {id_filter}, description {description}, category {category}, and status {status} updated successfully!"
    }

@app.route("/tasks/complete", methods =["PUT"])
def id_complete():
    id_filter = request.args.get("id", type=int)

    update = get_task_id(id_filter)

    if update is None:
        return {"error": "Task not found"}, 404

    update["status"]="completed"

    with open("data.json","r") as file:
        all_tasks_data=json.load(file)

    for task in all_tasks_data["tasks"]:
           if task['id']==id_filter:
               task.update(update)

    with open("data.json", "w") as file:
        json.dump(all_tasks_data, file, indent=4)
    return {
    'message': f"Task with ID {id_filter} changed status to completed successfully!"
}

@app.route("/tasks/categories", methods=["GET"])
def get_categories():

    with open("data.json", "r") as file:
         all_tasks_data = json.load(file)

    category_filter = request.args.get('category', default = None, type = str)

    if category_filter:
        filtred_tasks = [task for task in all_tasks_data["tasks"] if task.get('category') == category_filter]
        return jsonify({"tasks": filtred_tasks})

    unique_categories = list({task["category"] for task in all_tasks_data["tasks"] if "category" in task})
    return jsonify({"categories": unique_categories})

@app.route('/tasks/categories/<string:category_name>', methods=["GET"])
def category_with_tasks(category_name):
    with open("data.json",'r') as file:
        all_tasks_data = json.load(file)

       # category_filter = request.args.get('category', default=None, type=str)

    filtred_tasks = [task for task in all_tasks_data["tasks"] if task.get('category') == category_name]

    if filtred_tasks:
         return jsonify({"tasks": filtred_tasks})
    else:
        return jsonify({"message": f"No tasks found in category '{category_name}'"}), 404




if __name__ == '__main__':
    app.run(debug=True)

