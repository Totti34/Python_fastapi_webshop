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

    #Change to user_id parameter, 
    # #this way it is ensured that the data handling logic stays in DataManager.
    #The empty new basket created here, since the endpoint only takes usierid.
    def add_basket(self, user_id : int) -> None:
        data = self.load_json(DATA_FILE)
        baskets_list = data.get("Baskets", [])

        current_basket_id = 0

        for basket in baskets_list:
            current_basket_id = basket.get("id")
            
        new_basket={
            "id": current_basket_id+1,
            "user_id": user_id,
            "items" : []
        }

        data.setdefault("Baskets", []).append(new_basket)
        self.save_json(path=DATA_FILE,data=data)

    def add_item_to_basket(self, user_id: int, item: Dict[str, Any]) -> None:
        data = self.load_json(DATA_FILE)
        baskets_list = data.get("Baskets", [])
        exists = False

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                basket.setdefault("items", []).append(item)
                exists = True
                break
        if exists:
            self.save_json(DATA_FILE, data)
        else:
            raise ValueError(f"Nem létezik bevásárlókosár {user_id}-hoz!")


    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        data = self.load_json(USERS_FILE)
        users_list = data.get("Users", [])

        for user in users_list:
            if user.get("id") == user_id:
                return user
        return None

    def get_basket_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        data = self.load_json(DATA_FILE)
        baskets_list = data.get("Baskets", [])

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                return basket
        return None

    def get_all_users(self) -> List[Dict[str, Any]]:
        data = self.load_json(self.users_path)
        return data.get("Users", [])

    def get_total_price_of_basket(self,user_id: int) -> float:
        data = self.load_json(DATA_FILE)
        baskets_list = data.get("Baskets", [])

        total_price = 0.0
        
        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                items_list = basket.get("items", [])
                for item in items_list:
                    price = item.get("price", 0)
                    quantity = item.get("quantity", 0)
                    total_price += price * quantity
                
            break

        return total_price


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