import json
from typing import Dict, Any, List
from schemas.schema import User, Basket, Item


# A JSON fájl elérési útja
USERS_FILE = "data/users.json"
DATA_FILE = "data/data.json"

class DataManager:
    def __init__(self, users_file_path, data_file_path ):
        self.users_path = users_file_path
        self.data_path = data_file_path

    def load_json() -> Dict[str, Any]:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            pass

    def save_json(data: Dict[str, Any]) -> None:
        pass

    def add_user(user: Dict[str, Any]) -> None:
        pass

    def add_basket(basket: Dict[str, Any]) -> None:
        pass

    def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
        pass

    def get_user_by_id(user_id: int) -> Dict[str, Any]:
        pass

    def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
        pass

    def get_all_users() -> List[Dict[str, Any]]:
        pass

    def get_total_price_of_basket(user_id: int) -> float:
        pass

    def update_item_in_basket(user_id, item_id, updated_item) -> None:
        pass

    def delete_item_from_basket(user_id, item_id) -> None:
        pass

    def clear_basket(user_id) -> None:
        pass

    def is_basket_empty(user_id) -> bool:
        pass

    def delete_user(user_id) -> None:
        pass