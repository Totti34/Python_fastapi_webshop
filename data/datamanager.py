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
        except:
            if "users" in path:
                return {"Users": []}
            else:
                return {"Baskets": []}


    def save_json(self, path: str, data: Dict[str, Any], ) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_user(self, user: Dict[str, Any]) -> None:
        data = self.load_json(self.users_path)
        data.setdefault("Users", []).append(user)
        self.save_json(path=self.users_path,data=data)



    #Change to user_id parameter, 
    # #this way it is ensured that the data handling logic stays in DataManager.
    #The empty new basket created here, since the endpoint only takes usierid.
    def add_basket(self, user_id : int) -> None:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])

        max_id = 0

        for basket in baskets_list:
            current_id = basket.get("id", 0)
            if current_id > max_id:
                max_id = current_id
            
        if max_id == 0:
            new_id = 101
        else:
            new_id = max_id + 1

        new_basket={
            "id": new_id,
            "user_id": user_id,
            "items" : []
        }

        data.setdefault("Baskets", []).append(new_basket)
        self.save_json(path=self.data_path,data=data)



    def add_item_to_basket(self, user_id: int, item: Dict[str, Any]) -> None:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])
        exists = False

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                basket.setdefault("items", []).append(item)
                exists = True
                break
        if exists:
            self.save_json(self.data_path, data)
        else:
            raise ValueError(f"Nem létezik bevásárlókosár {user_id}-hoz!")



    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        data = self.load_json(self.users_path)
        users_list = data.get("Users", [])

        for user in users_list:
            if user.get("id") == user_id:
                return user
        return None



    def get_basket_by_user_id(self, user_id: int) -> List[Dict[str, Any]]:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])
        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                return basket.get("items", [])
        return None



    def get_all_users(self) -> List[Dict[str, Any]]:
        data = self.load_json(self.users_path)
        return data.get("Users", [])



    def get_total_price_of_basket(self,user_id: int) -> float:
        total_price = 0.0
        basket = self.get_basket_by_user_id(user_id)

        if basket is not None:
            for item in basket:
                price = item.get("price", 0)
                quantity = item.get("quantity", 0)
                total_price += price * quantity
        
        return total_price



    def update_item_in_basket(self, user_id: int, item_id: int, updated_item: Dict[str, Any]) -> None:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])
        exists_basket = False
        exists_item = False

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                item_list = basket.get("items", [])
                exists_basket = True
                for item in item_list:
                    if item.get("item_id") == item_id:
                        item.update(updated_item)
                        exists_item = True
                        break
        
        if exists_basket and exists_item:
            self.save_json(self.data_path, data)
        elif exists_basket:
            raise ValueError(f"Nem létezik {item_id} tétel {user_id} bevásárlókosarában!")
        else:
             raise ValueError(f"Nem létezik bevásárlókosár {user_id}-hoz!")



    def delete_item_from_basket(self, user_id, item_id) -> None:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])
        exists_basket = False
        exists_item = False

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                item_list = basket.get("items", [])
                exists_basket = True
                for i, item in enumerate(item_list):
                    if item.get("item_id") == item_id:
                        item_list.pop(i)
                        exists_item = True
                        break

        if exists_basket and exists_item:
            self.save_json(self.data_path, data)
        elif exists_basket:
            raise ValueError(f"Nem lehet törölni, mivel nem létezik itemid:{item_id} tétel userid:{user_id} bevásárlókosarában!")
        else:
             raise ValueError(f"Nem tartozik bevásárlókosár userid:{user_id}-hoz!")
        


    def clear_basket(self, user_id) -> None:
        data = self.load_json(self.data_path)
        baskets_list = data.get("Baskets", [])
        exists_basket = False

        for basket in baskets_list:
            if basket.get("user_id") == user_id:
                basket["items"] = []
                exists_basket = True
                break

        if exists_basket:
            self.save_json(self.data_path, data)
        else:
             raise ValueError(f"Nem tartozik bevásárlókosár userid:{user_id}-hoz!")



    def delete_user(self,user_id) -> None:
        user_basket = self.get_basket_by_user_id(user_id)

        if not user_basket:
            data = self.load_json(self.users_path)
            users_list = data.get("Users", []) 
            for i, user in enumerate(users_list):
                if user.get("id") == user_id:
                    users_list.pop(i)
                    self.save_json(self.users_path, data=data)
                    break
        
        else:
            raise ValueError("A kosár nem üres, a felhasználó nem törölhető.")