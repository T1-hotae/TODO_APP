import requests

BASE_URL = "http://localhost:8000/api/todos"

def get_all_todos():
    try:
        return requests.get(BASE_URL).json()
    except Exception:
        return []

def add_todo(title: str):
    return requests.post(BASE_URL + "/", json={"title": title}).json()

def toggle_todo(todo_id: int):
    todos = get_all_todos()
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo:
        requests.patch(f"{BASE_URL}/{todo_id}", json={"is_completed": not todo["is_completed"]})

def delete_todo(todo_id: int):
    requests.delete(f"{BASE_URL}/{todo_id}")
