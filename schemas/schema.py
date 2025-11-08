from pydantic import BaseModel, EmailStr, field_validator
from typing import List


ShopName='Webshop'


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    @field_validator("email")
    def check_email(cls, email):
        if not isinstance(email, EmailStr):
            return ValueError("Error: This is not a valid email format!")
        return email
    
    @field_validator("id")
    def check_id(cls, id):
        if id < 0:
            return ValueError("Error: This is not a valid id!")
        return id


class Item(BaseModel):
    item_id: int
    name: str
    brand: str
    price: float
    quantity: int

    @field_validator("item_id")
    def check_item_id(cls, item_id):
        if item_id < 0:
            return ValueError("Error: This is not a valid item_id!")
        return item_id
    
    @field_validator("quantity")
    def check_quantity(cls, quantity):
        if id < 0:
            return ValueError("Error: This is not a valid quantity!")
        return quantity
    
    @field_validator("price")
    def check_price(cls, price):
        if price < 0:
            raise ValueError("Error: Price cannot be negative!")
        return price


class Basket(BaseModel):
    id: int
    user_id: int
    items: List[Item]

    @field_validator("id")
    def check_id(cls, id):
        if id < 0:
            return ValueError("Error: This is not a valid id!")
        return id
    
    @field_validator("user_id")
    def check_user_id(cls, user_id):
        if user_id < 0:
            return ValueError("Error: This is not a valid user_id!")
        return user_id