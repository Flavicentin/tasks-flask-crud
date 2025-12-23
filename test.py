import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []

# teste criando tarefa
def test_create_task():
    new_task_data = {
        "title": "nova tarefa",
        "description": "descrição nova tarefa"
    }

    # valida status
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200

    # valida json
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])


# teste lendo tarefas
def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200

    print(response)

    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json


# teste pegando uma tarefa [id]
def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response_json = response.json()
        assert task_id == response_json['id']


# teste update taks
def test_update_task():
    if tasks:
        task_id = tasks[0]
        paylaod = {
            "title": "Novo Titulo (update)",
            "description": "Nova Descrição (update)",
            "completed": True
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=paylaod)
        assert response.status_code == 200

        response_json = response.json()
        assert "message" in response_json

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response_json = response.json()
        assert response_json["title"] == paylaod["title"]
        assert response_json["description"] == paylaod["description"]
        assert response_json["completed"] == paylaod["completed"]


# teste deletando tarefa
def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404