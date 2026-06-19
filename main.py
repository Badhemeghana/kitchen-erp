from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import engine, SessionLocal, Base

# Create all tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Home Kitchen ERP")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== USERS ==========
@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_name(db, user.name)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, user)

@app.get("/users", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/login")
def login(name: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_name(db, name)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Wrong name or password")
    return {"id": user.id, "name": user.name, "role": user.role}

# ========== INVENTORY ==========
@app.get("/inventory", response_model=List[schemas.InventoryOut])
def list_inventory(db: Session = Depends(get_db)):
    return crud.get_inventory(db)

@app.post("/inventory", response_model=schemas.InventoryOut)
def add_inventory(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_item(db, item)

@app.delete("/inventory/{item_id}")
def remove_inventory(item_id: int, db: Session = Depends(get_db)):
    crud.delete_inventory_item(db, item_id)
    return {"ok": True}

# ========== RECIPES ==========
@app.get("/recipes", response_model=List[schemas.RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    return crud.get_recipes(db)

@app.post("/recipes", response_model=schemas.RecipeOut)
def add_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@app.delete("/recipes/{recipe_id}")
def remove_recipe(recipe_id: int, db: Session = Depends(get_db)):
    crud.delete_recipe(db, recipe_id)
    return {"ok": True}

# ========== MEAL PLAN ==========
@app.get("/mealplan", response_model=List[schemas.MealPlanOut])
def list_mealplan(db: Session = Depends(get_db)):
    return crud.get_meal_plan(db)

@app.post("/mealplan", response_model=schemas.MealPlanOut)
def add_mealplan(plan: schemas.MealPlanCreate, db: Session = Depends(get_db)):
    return crud.create_meal_plan(db, plan)

# ========== SHOPPING ==========
@app.get("/shopping", response_model=List[schemas.ShoppingOut])
def list_shopping(db: Session = Depends(get_db)):
    return crud.get_shopping(db)

@app.post("/shopping", response_model=schemas.ShoppingOut)
def add_shopping(item: schemas.ShoppingCreate, db: Session = Depends(get_db)):
    return crud.create_shopping_item(db, item)

@app.put("/shopping/{item_id}/toggle")
def toggle_shopping(item_id: int, db: Session = Depends(get_db)):
    crud.toggle_shopping_item(db, item_id)
    return {"ok": True}

@app.delete("/shopping/{item_id}")
def remove_shopping(item_id: int, db: Session = Depends(get_db)):
    crud.delete_shopping_item(db, item_id)
    return {"ok": True}
from voice import understand_command

@app.post("/voice-command")
def voice_command(payload: dict, db: Session = Depends(get_db)):
    text = payload.get("text", "")
    if not text:
        return {"success": False, "message": "No text received"}

    result = understand_command(text)
    action = result["action"]
    item_name = result["item"]

    if not item_name:
        return {"success": False, "message": "Could not understand"}

    if action == "pantry":
        item = schemas.InventoryCreate(name=item_name)
        crud.create_inventory_item(db, item)
        return {"success": True, "action": "pantry", "item": item_name,
                "message": f"✅ '{item_name}' Pantry కి add అయింది!"}
    else:
        item = schemas.ShoppingCreate(item_name=item_name)
        crud.create_shopping_item(db, item)
        return {"success": True, "action": "shopping", "item": item_name,
                "message": f"🛒 '{item_name}' Shopping list కి add అయింది!"}
@app.put("/users/{user_id}/password")
def update_password(user_id: int, new_password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.password = new_password
        db.commit()
        return {"ok": True, "message": "Password updated"}
    raise HTTPException(status_code=404, detail="User not found")