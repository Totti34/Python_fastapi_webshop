from schemas.schema import User, Basket, Item
from data.datamanager import DataManager
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie, status
from fastapi import APIRouter

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

routers = APIRouter()
manage_data = DataManager()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try:
        user_dictionary = user.model_dump()
        manage_data.add_user(user_dictionary)
        
        return JSONResponse(content=user_dictionary, status_code=201)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Internal server error: {str(e)}"
        )


@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    pass

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    pass

@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    pass

@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    pass

@routers.get('/user')
def user(userid: int) -> User:
    return manage_data.get_user_by_id(userid)

@routers.get('/users')
def users() -> list[User]:
    user_data = manage_data.get_all_users()
    return user_data

@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    pass

@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    pass
