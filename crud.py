from sqlalchemy.orm import Session
import models, schemas

# ---- Users ----
def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---- Inventory ----
def get_inventory(db: Session):
    return db.query(models.InventoryItem).all()

def create_inventory_item(db: Session, item: schemas.InventoryCreate):
    db_item = models.InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_inventory_item(db: Session, item_id: int):
    item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

# ---- Recipes ----
def get_recipes(db: Session):
    return db.query(models.Recipe).all()

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe

# ---- Meal Plan ----
def get_meal_plan(db: Session):
    return db.query(models.MealPlan).all()

def create_meal_plan(db: Session, plan: schemas.MealPlanCreate):
    existing = db.query(models.MealPlan).filter(
        models.MealPlan.day_of_week == plan.day_of_week
    ).first()
    if existing:
        db.delete(existing)
        db.commit()
    db_plan = models.MealPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# ---- Shopping ----
def get_shopping(db: Session):
    return db.query(models.ShoppingItem).all()

def create_shopping_item(db: Session, item: schemas.ShoppingCreate):
    db_item = models.ShoppingItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def toggle_shopping_item(db: Session, item_id: int):
    item = db.query(models.ShoppingItem).filter(
        models.ShoppingItem.id == item_id
    ).first()
    if item:
        item.is_purchased = not item.is_purchased
        db.commit()
        db.refresh(item)
    return item

def delete_shopping_item(db: Session, item_id: int):
    item = db.query(models.ShoppingItem).filter(
        models.ShoppingItem.id == item_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return item