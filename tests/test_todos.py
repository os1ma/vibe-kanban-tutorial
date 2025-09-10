import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from app.main import app
from app.database import Base, get_db
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

class TestTodoAPI:
    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Welcome to TODO API"

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_todo(self):
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "priority": "high",
            "category": "work",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat()
        }
        response = client.post("/todos/", json=todo_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == todo_data["title"]
        assert data["description"] == todo_data["description"]
        assert data["priority"] == todo_data["priority"]
        assert data["category"] == todo_data["category"]
        assert data["status"] == False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_read_todos(self):
        todo_data = {"title": "Test Todo 1", "priority": "medium"}
        client.post("/todos/", json=todo_data)
        todo_data = {"title": "Test Todo 2", "priority": "high"}
        client.post("/todos/", json=todo_data)
        
        response = client.get("/todos/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Test Todo 1"
        assert data[1]["title"] == "Test Todo 2"

    def test_read_todo(self):
        todo_data = {"title": "Test Todo", "priority": "low"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        response = client.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == todo_data["title"]

    def test_read_todo_not_found(self):
        response = client.get("/todos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_update_todo(self):
        todo_data = {"title": "Original Title", "priority": "low"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        update_data = {
            "title": "Updated Title",
            "status": True,
            "priority": "high"
        }
        response = client.put(f"/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["status"] == update_data["status"]
        assert data["priority"] == update_data["priority"]

    def test_update_todo_not_found(self):
        update_data = {"title": "Updated Title"}
        response = client.put("/todos/999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_delete_todo(self):
        todo_data = {"title": "To be deleted", "priority": "medium"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        response = client.delete(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self):
        response = client.delete("/todos/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Todo not found"

    def test_filter_todos_by_status(self):
        client.post("/todos/", json={"title": "Todo 1", "priority": "medium"})
        client.post("/todos/", json={"title": "Todo 2", "priority": "high"})
        
        todo_data = {"title": "Todo 3", "priority": "low"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        client.put(f"/todos/{todo_id}", json={"status": True})
        
        response = client.get("/todos/filter?status=completed")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == True
        
        response = client.get("/todos/filter?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(not todo["status"] for todo in data)

    def test_filter_todos_by_priority(self):
        client.post("/todos/", json={"title": "High Priority", "priority": "high"})
        client.post("/todos/", json={"title": "Medium Priority", "priority": "medium"})
        client.post("/todos/", json={"title": "Low Priority", "priority": "low"})
        
        response = client.get("/todos/filter?priority=high")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["priority"] == "high"

    def test_filter_todos_by_category(self):
        client.post("/todos/", json={"title": "Work Task", "priority": "high", "category": "work"})
        client.post("/todos/", json={"title": "Personal Task", "priority": "medium", "category": "personal"})
        client.post("/todos/", json={"title": "Work Task 2", "priority": "low", "category": "work"})
        
        response = client.get("/todos/filter?category=work")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(todo["category"] == "work" for todo in data)

    def test_pagination(self):
        for i in range(5):
            client.post("/todos/", json={"title": f"Todo {i+1}", "priority": "medium"})
        
        response = client.get("/todos/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Todo 3"
        assert data[1]["title"] == "Todo 4"

    def test_invalid_priority(self):
        todo_data = {"title": "Invalid Priority", "priority": "invalid"}
        response = client.post("/todos/", json=todo_data)
        assert response.status_code == 422

    def test_empty_title(self):
        todo_data = {"title": "", "priority": "medium"}
        response = client.post("/todos/", json=todo_data)
        assert response.status_code == 422