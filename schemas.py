from pydantic import BaseModel
from typing import Optional
from datetime import date

# ---- User ----
class UserCreate(BaseModel):
    name: str
    role: str = "member"
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    role: str
    class Config:
        from_attributes = True

# ---- Inventory ----
class InventoryCreate(BaseModel):
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    expiry_date: Optional[date] = None
    category: Optional[str] = None

class InventoryOut(InventoryCreate):
    id: int
    class Config:
        from_attributes = True

# ---- Recipe ----
class RecipeCreate(BaseModel):
    name: str
    instructions: Optional[str] = None
    created_by: Optional[int] = None

class RecipeOut(RecipeCreate):
    id: int
    class Config:
        from_attributes = True

# ---- Recipe Ingredient ----
class IngredientCreate(BaseModel):
    recipe_id: int
    item_name: str
    quantity: Optional[str] = None

class IngredientOut(IngredientCreate):
    id: int
    class Config:
        from_attributes = True

# ---- Meal Plan ----
class MealPlanCreate(BaseModel):
    day_of_week: str
    recipe_id: Optional[int] = None
    planned_by: Optional[int] = None

class MealPlanOut(MealPlanCreate):
    id: int
    class Config:
        from_attributes = True

# ---- Shopping ----
class ShoppingCreate(BaseModel):
    item_name: str
    estimated_cost: float = 0
    added_by: Optional[int] = None

class ShoppingOut(ShoppingCreate):
    id: int
    is_purchased: bool
    class Config:
        from_attributes = True