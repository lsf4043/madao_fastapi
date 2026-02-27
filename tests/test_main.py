import pytest
from fastapi.testclient import TestClient
from app import main
from app.main import app, fake_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    fake_db.clear()
    main.item_id_counter = 0
    yield

class TestRootEndpoint:
    def test_root_returns_welcome_message(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Madao FastAPI Test Project"}

class TestCreateItem:
    def test_create_item_without_tax(self):
        item_data = {
            "name": "Test Item",
            "description": "A test item",
            "price": 10.5
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Test Item"
        assert data["description"] == "A test item"
        assert data["price"] == 10.5
        assert data["price_with_tax"] == 10.5
    
    def test_create_item_with_tax(self):
        item_data = {
            "name": "Taxed Item",
            "price": 100.0,
            "tax": 10.0
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Taxed Item"
        assert data["price"] == 100.0
        assert data["tax"] == 10.0
        assert data["price_with_tax"] == 110.0
    
    def test_create_item_missing_required_field(self):
        item_data = {
            "description": "Missing name and price"
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 422

class TestReadItem:
    def test_read_existing_item(self):
        create_data = {
            "name": "Read Test",
            "price": 50.0
        }
        create_response = client.post("/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Read Test"
        assert data["price"] == 50.0
    
    def test_read_nonexistent_item(self):
        response = client.get("/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"

class TestUpdateItem:
    def test_update_existing_item(self):
        create_data = {
            "name": "Original Name",
            "price": 20.0
        }
        create_response = client.post("/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        update_data = {
            "name": "Updated Name",
            "price": 25.0,
            "tax": 2.5
        }
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["price"] == 25.0
        assert data["tax"] == 2.5
        assert data["price_with_tax"] == 27.5
    
    def test_update_nonexistent_item(self):
        update_data = {
            "name": "Ghost Item",
            "price": 0.0
        }
        response = client.put("/items/999", json=update_data)
        assert response.status_code == 404

class TestDeleteItem:
    def test_delete_existing_item(self):
        create_data = {
            "name": "To Be Deleted",
            "price": 15.0
        }
        create_response = client.post("/items/", json=create_data)
        item_id = create_response.json()["id"]
        
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_item(self):
        response = client.delete("/items/999")
        assert response.status_code == 404

class TestListItems:
    def test_list_empty_items(self):
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == {"items": [], "total": 0}
    
    def test_list_multiple_items(self):
        items = [
            {"name": "Item 1", "price": 10.0},
            {"name": "Item 2", "price": 20.0},
            {"name": "Item 3", "price": 30.0}
        ]
        
        for item in items:
            client.post("/items/", json=item)
        
        response = client.get("/items/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3
