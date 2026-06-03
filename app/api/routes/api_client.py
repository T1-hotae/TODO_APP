import requests

BASE_URL = "http://localhost:8000/api/todos"

def get_all_todos():
    try:
        response = requests.get(BASE_URL)
        return response.json()
    except Exception as e:
        return []

def add_todo(title, content, priority, category):
    data = {
        "title": title,
        "content": content,
        "priority": priority,
        "category": category
    }
    response = requests.post(BASE_URL + "/", json=data)
    return response.json()

def toggle_todo(todo_id, is_completed):
    response = requests.patch(f"{BASE_URL}/{todo_id}", json={"is_completed": not is_completed})
    return response.json()