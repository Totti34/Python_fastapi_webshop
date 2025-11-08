import json
from typing import Dict, Any, List
from schemas.schema import User, Basket, Item


# JSON data files path
USERS_FILE = "data/users.json"
DATA_FILE = "data/data.json"

class DataManager:
    def __init__(self):
        self.users_path = USERS_FILE
        self.data_path = DATA_FILE

    def load_json(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(path)
        except FileNotFoundError:
            if "users" in path:
                return {"Users": []}
            else:
                return {"Baskets": []}
        except:
            return{}


    def save_json(self, path: str, data: Dict[str, Any], ) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_user(self, user: Dict[str, Any]) -> None:
        data = self.load_json(USERS_FILE)
        data.update(user)
        self.save_json(USERS_FILE,data=data)

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

test = DataManager()

test.add_user()