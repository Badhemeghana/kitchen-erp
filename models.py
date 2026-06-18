from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, default="member")
    password = Column(String, nullable=False)

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(String)
    unit = Column(String)
    expiry_date = Column(Date)
    category = Column(String)

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructions = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    item_name = Column(String, nullable=False)
    quantity = Column(String)

class MealPlan(Base):
    __tablename__ = "meal_plan"
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    planned_by = Column(Integer, ForeignKey("users.id"))

class ShoppingItem(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    estimated_cost = Column(Float, default=0)
    is_purchased = Column(Boolean, default=False)
    added_by = Column(Integer, ForeignKey("users.id"))