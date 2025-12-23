from flask import request, Flask, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1


# cria tarefa 
@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()

    new_task = Task(id=task_id_control,title = data.get("title", ""),description = data.get("description", ""))

    tasks.append(new_task)
    task_id_control += 1

    return jsonify({"message": "Nova Tarefa Criada Com Sucesso!", "id": new_task.id})


# pega tarefas 
@app.route("/tasks", methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)


# pega tarefa pelo (id)
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
  
    return jsonify({"message": "Não foi possível encontrar a atividade"}), 404


# update
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task.title = data.get("title")
    task.description = data.get("description")
    task.completed = data.get("completed")
    
    return jsonify({"message": "Tarefa Atualizada!"})


# delete
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa Deletada!"})

if __name__ == "__main__":
    app.run(debug=True)