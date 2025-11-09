from schemas.schema import User, Basket, Item
from data.datamanager import DataManager
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie, status, Depends, APIRouter
from authentication.authentication import verify_token

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''
###-------------------------------------------------ADMIN endpoints-------------------------------------------------###

routers = APIRouter()
manage_data = DataManager()

@routers.post('/adduser', response_model=User, dependencies=[Depends(verify_token)])
def adduser(user: User) -> User:
    try:
        user_dictionary = user.model_dump()
        manage_data.add_user(user_dictionary)
        return JSONResponse(content=user_dictionary, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.get('/user', dependencies=[Depends(verify_token)])
def user(userid: int) -> User:
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
    try:
        user_data = manage_data.get_all_users()
        return JSONResponse(content=user_data, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))



@routers.post('/addshoppingbag', dependencies=[Depends(verify_token)])
def addshoppingbag(userid: int) -> str:
    existing_basket = manage_data.get_basket_by_user_id(userid)

    if existing_basket is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"userid: {userid} már rendelkezik kosárral!")
    
    try:
        manage_data.add_basket(userid) 
        return JSONResponse(content="Sikeres kosár hozzárendelés.", status_code=status.HTTP_201_CREATED)
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.delete('/deletall', dependencies=[Depends(verify_token)])
def deleteall(userid: int) -> Basket:
    try:
        manage_data.clear_basket(userid)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=201)
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@routers.delete('/deleteuser', dependencies=[Depends(verify_token)])
def deleteuser(userid: int) -> str:
    try:
        manage_data.delete_user(userid)
        return JSONResponse(content=f"Felhasználó userid:{userid} sikeresen törölve", status_code=status.HTTP_202_ACCEPTED)
    
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail=str(e))



###-------------------------------------------------OTHER endpoints-------------------------------------------------###



@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    item_dictionary = item.model_dump()

    try:
        manage_data.add_item_to_basket(userid, item_dictionary)
        basket_dictionary = manage_data.get_basket_by_user_id(userid)
        return JSONResponse(content=basket_dictionary, status_code=status.HTTP_201_CREATED)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    try:
        content = manage_data.get_basket_by_user_id(userid)
        if content is not None:
            return JSONResponse(content= content, status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nem tartozik kosár userid:{userid}-hez!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        


@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    try:
        content = manage_data.get_total_price_of_basket(userid)
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        item_dictionary = updateItem.model_dump()
        manage_data.update_item_in_basket(userid, itemid, item_dictionary)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=201)
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        manage_data.delete_item_from_basket(userid, itemid)
        return JSONResponse(content=manage_data.get_basket_by_user_id(userid), status_code=201)
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail=str(e))