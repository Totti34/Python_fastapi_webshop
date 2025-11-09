from schemas.schema import User, Basket, Item
from data.datamanager import DataManager
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie, status, Depends, APIRouter
from authentication.authentication import verify_token

'''
A jelenlegi fájl tartalmazza a feladathoz szükséges végpontokat.
Minden végpont try-except blokk-ból épül fel, ezáltal biztosított, 
hogy bármilyen váratlan hiba esetén továbbra is működőképes marad a program.
Néhány végponton, ahol volt értelme, implementálásra került extra HTTPException dobás.
'''
###-------------------------------------------------ADMIN endpoints-------------------------------------------------###

routers = APIRouter()
manage_data = DataManager()

@routers.post('/adduser', response_model=User, dependencies=[Depends(verify_token)])
def adduser(user: User) -> User:
    """
    Visszaadja az összes regisztrált felhasználót.
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """

    try:
        user_dictionary = user.model_dump()
        manage_data.add_user(user_dictionary)
        return JSONResponse(content=user_dictionary, status_code=status.HTTP_201_CREATED)
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.get('/user', dependencies=[Depends(verify_token)])
def user(userid: int) -> User:
    """
    Egy adott felhasználó adatainak lekérdezése azonosító (userid) alapján.
    Hibát dob (404 Not found), ha nincs ilyen azanosítóval rendelkező felhasználó.
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """

    try:
        user = manage_data.get_user_by_id(userid)
        if user is not None:
            return JSONResponse(content=user, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nincs userid:{userid} rendelkező user!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@routers.get('/users', dependencies=[Depends(verify_token)])
def users() -> list[User]:
    """
    Visszaadja az összes regisztrált felhasználót.
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """

    try:
        user_data = manage_data.get_all_users()
        return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@routers.post('/addshoppingbag', dependencies=[Depends(verify_token)])
def addshoppingbag(userid: int) -> str:
    """
    Létrehoz egy új, üres bevásárlókosarat a megadott felhasználóhoz.
    Hibát dob (409 Conflict), ha a felhasználónak már van kosara.
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """
    
    try:
        existing_basket = manage_data.get_basket_by_user_id(userid)
        if existing_basket is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"userid: {userid} már rendelkezik kosárral!")
        
        manage_data.add_basket(userid) 
        return JSONResponse(content="Sikeres kosár hozzárendelés.", status_code=status.HTTP_201_CREATED)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.delete('/deletall', dependencies=[Depends(verify_token)])
def deleteall(userid: int) -> Basket:
    """
    Törli a megadott felhasználó (userid alapján) kosarának teljes tartalmát (az összes terméket).
    A kiürített kosár tartalmát adja vissza (üres listával).
    Hibát dob (404 Not found), ha nincs bevásárlókosara ezzel az azonosítóval rendelkező 
    felhasználónak (tehát ha a felhasználó sem létezik).
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """

    try:
        manage_data.clear_basket(userid)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=status.HTTP_200_OK)
    
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.delete('/deleteuser', dependencies=[Depends(verify_token)])
def deleteuser(userid: int) -> str:
    """
    Törli a megadott felhasználót a rendszerből.
    A törlés csak akkor sikeres, ha a felhasználó kosara üres vagy nem létezik.
    Hibát dob (409 Conflict), ha a felhasználónak nem üres a kosara.
    Ez egy adminisztrátori funkció, érvényes token szükséges.
    """

    try:
        manage_data.delete_user(userid)
        return JSONResponse(content=f"Felhasználó userid:{userid} sikeresen törölve", status_code=status.HTTP_200_OK)
    
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



###-------------------------------------------------OTHER endpoints-------------------------------------------------###



@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    """
    Hozzáad egy új terméket a megadott felhasználó (userid) kosarához.
    Sikeres hozzáadás esetén a teljes, frissített kosár tartalmát adja vissza.
    """

    item_dictionary = item.model_dump()

    try:
        manage_data.add_item_to_basket(userid, item_dictionary)
        basket_dictionary = manage_data.get_basket_by_user_id(userid)
        return JSONResponse(content=basket_dictionary, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    """
    Visszaadja egy adott felhasználó (userid) kosarának teljes tartalmát (az összes terméket).
    Ha a felhasználónak van kosara, de az üres, egy üres listát ad vissza.
    Hibát dob (404 Not Found), ha a felhasználóhoz nem tartozik kosár (vagy maga a felhasználó nem létezik).
    """
    try:
        content = manage_data.get_basket_by_user_id(userid)
        if content is not None:
            return JSONResponse(content= content, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nem tartozik kosár userid:{userid}-hez, vagy nincs is ilyen felhasználó!")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        


@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    """
    Visszaadja a megadott felhasználó (userid) kosarában lévő összes termék összértékét (price * quantity).
    Ha a felhasználónak nincs kosara, vagy a kosár üres, 0.0-t ad vissza.
    """

    try:
        content = manage_data.get_total_price_of_basket(userid)
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    """
    Módosítja egy meglévő termék (itemid) adatait a megadott felhasználó (userid) kosarában.
    Sikeres módosítás esetén a teljes, frissített kosár tartalmát adja vissza.
    Hibát dob (404 Not Found), nincs ezzel az azonosítóval rendelkező item vagy felhasználó.
    """

    try:
        item_dictionary = updateItem.model_dump()
        manage_data.update_item_in_basket(userid, itemid, item_dictionary)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=201)
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    """
    Töröl egy adott terméket (itemid) a megadott felhasználó (userid) kosarából.
    Sikeres törlés esetén a teljes, frissített kosár tartalmát adja vissza.
    Hibát dob (404 Not Found), nincs ezzel az azonosítóval rendelkező item vagy felhasználó.
    """

    try:
        manage_data.delete_item_from_basket(userid, itemid)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=201)
    
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))