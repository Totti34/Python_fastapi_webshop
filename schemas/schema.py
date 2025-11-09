from pydantic import BaseModel, EmailStr, field_validator
from typing import List



"""
A jelenlegi fájl tartalmazza a feladathoz szükséges összes adatmodellt (sémát).

Ezek a Pydantic BaseModel-re épülő osztályok (User, Item, Basket) definiálják
az API végpontok által várt bemeneti (request body) és kimeneti (response_model)
adatstruktúrákat.

Minden modell beépített validátorokat (@field_validator) használ,
ezáltal biztosított, hogy az adatok megfeleljenek az üzleti logikának
(pl. ID-k és árak nem lehetnek negatívak).

Validációs hiba esetén a modellek 'ValueError'-t dobnak,
amit a FastAPI automatikusan elkap és '422 Unprocessable Entity'
HTTP hibaként küld vissza a kliensnek.
"""



ShopName='Webshop'


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    @field_validator("id")
    def check_id(cls, id):
        if id < 0:
            raise ValueError("A userid csak pozitív lehet!")
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
            raise ValueError("Az itemid csak pozitív lehet!")
        return item_id
    
    @field_validator("quantity")
    def check_quantity(cls, quantity):
        if quantity < 0:
            raise ValueError("A quantity csak pozitív lehet!")
        return quantity
    
    @field_validator("price")
    def check_price(cls, price):
        if price < 0:
            raise ValueError("A price csak pozitív lehet!")
        return price


class Basket(BaseModel):
    id: int
    user_id: int
    items: List[Item]

    @field_validator("id")
    def check_id(cls, id):
        if id < 0:
            raise ValueError("A basketid csak pozitív lehet!")
        return id
    
    @field_validator("user_id")
    def check_user_id(cls, user_id):
        if user_id < 0:
            raise ValueError("A userid csak pozitív lehet!")
        return user_id