def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ZenTodo"}

def test_create_todo(client):
    payload = {
        "title": "테스트 할 일",
        "content": "이것은 단위 테스트입니다.",
        "priority": "High",
        "category": "Work",
        "due_date": "2026-06-10"
    }
    response = client.post("/api/todos", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "테스트 할 일"
    assert data["content"] == "이것은 단위 테스트입니다."
    assert data["priority"] == "High"
    assert data["category"] == "Work"
    assert data["due_date"] == "2026-06-10"
    assert data["is_completed"] is False
    assert data["d_day"] is not None

def test_read_todos(client):
    # 두 개의 투두 생성
    client.post("/api/todos", json={"title": "할 일 1", "priority": "Low"})
    client.post("/api/todos", json={"title": "할 일 2", "priority": "High"})

    # 전체 조회
    response = client.get("/api/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # 정렬 조회 (우선순위순 - High 우선)
    response_sorted = client.get("/api/todos?sort_by=priority")
    assert response_sorted.status_code == 200
    sorted_data = response_sorted.json()
    assert sorted_data[0]["title"] == "할 일 2" # High
    assert sorted_data[1]["title"] == "할 일 1" # Low

def test_update_todo(client):
    # 투두 생성
    res_create = client.post("/api/todos", json={"title": "원래 할 일"})
    todo_id = res_create.json()["id"]

    # 업데이트 요청
    payload = {"title": "수정된 할 일", "is_completed": True}
    response = client.put(f"/api/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "수정된 할 일"
    assert data["is_completed"] is True

def test_delete_todo(client):
    # 투두 생성
    res_create = client.post("/api/todos", json={"title": "삭제할 할 일"})
    todo_id = res_create.json()["id"]

    # 삭제 요청
    res_delete = client.delete(f"/api/todos/{todo_id}")
    assert res_delete.status_code == 204

    # 다시 단건 조회 시 404 확인
    res_get = client.get(f"/api/todos/{todo_id}")
    assert res_get.status_code == 404
