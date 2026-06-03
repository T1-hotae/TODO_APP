import requests

BASE_URL = "http://localhost:8000/api"
TODOS_URL = f"{BASE_URL}/todos"

def get_all_todos():
    try:
        return requests.get(TODOS_URL).json()
    except Exception:
        return []

def add_todo(title: str, due_date: str | None = None):
    payload = {"title": title}
    if due_date:
        payload["due_date"] = due_date
    return requests.post(TODOS_URL + "/", json=payload).json()

def toggle_todo(todo_id: int):
    todos = get_all_todos()
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo:
        requests.patch(f"{TODOS_URL}/{todo_id}", json={"is_completed": not todo["is_completed"]})

def delete_todo(todo_id: int):
    requests.delete(f"{TODOS_URL}/{todo_id}")

def update_todo_title(todo_id: int, title: str):
    return requests.patch(f"{TODOS_URL}/{todo_id}", json={"title": title}).json()

def ask_question(question: str) -> str:
    try:
        res = requests.post(f"{BASE_URL}/ask", json={"question": question})
        return res.json().get("answer", "응답을 가져올 수 없습니다.")
    except Exception as e:
        return f"오류: {e}"
