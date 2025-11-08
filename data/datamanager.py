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
                return json.load(file)
        except FileNotFoundError:
            if "users" in path:
                return {"Users": []}
            else:
                return {"Baskets": []}
        except:
            return {}


    def save_json(self, path: str, data: Dict[str, Any], ) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_user(self, user: Dict[str, Any]) -> None:
        data = self.load_json(USERS_FILE)
        data.setdefault("Users", []).append(user)
        self.save_json(path=USERS_FILE,data=data)

    def add_basket(basket: Dict[str, Any]) -> None:
        pass

    def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
        pass

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        data = self.load_json(USERS_FILE)
        users_list = data.get("Users", [])

        for user in users_list:
            if user.get("id") == user_id:
                return user
        return None

    def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
        pass

    def get_all_users(self) -> List[Dict[str, Any]]:
        data = self.load_json(self.users_path)
        return data.get("Users", [])

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