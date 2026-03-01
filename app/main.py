from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Madao FastAPI Test Project")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    price_with_tax: Optional[float] = None

fake_db = {}
item_id_counter = 0

@app.get("/")
async def root():
    return {"message": "11111111111Welcome to Madao FastAPI Test Project"}

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    global item_id_counter
    item_id_counter += 1
    
    item_dict = item.model_dump()
    item_dict["id"] = item_id_counter
    
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax
    else:
        item_dict["price_with_tax"] = item.price
    
    fake_db[item_id_counter] = item_dict
    return item_dict

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax
    else:
        item_dict["price_with_tax"] = item.price
    
    fake_db[item_id] = item_dict
    return item_dict

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = fake_db.pop(item_id)
    return {"message": f"Item '{deleted_item['name']}' deleted successfully"}

@app.get("/items/")
async def list_items():
    return {"items": list(fake_db.values()), "total": len(fake_db)}
