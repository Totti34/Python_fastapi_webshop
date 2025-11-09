Az alkalmazás architektúrája:

1. **`main.py`**: A fő FastAPI alkalmazásfájl. Ez indítja el az Uvicorn szervert és tölti be a `routers/routes.py`-ban definiált végpontokat.

2. **`schemas/schema.py`**: A Pydantic adatmodellek (`User`, `Item`, `Basket`) definíciója. Ez a réteg felel az adatok validálásáért is (pl. hogy az ID-k pozitívak, az e-mail címek érvényesek)

3. **`data/datamanager.py`**: A központi adatkezelő osztály (`DataManager`). Ez a "Service" réteg felel minden fájlműveletért (JSON olvasás/írás) és az üzleti logikáért. Kommunikál a `users.json` és `data.json` fájlokkal.

4. **`routers/routes.py`**: Az összes API végpont (`@routers.get`, `@routers.post` stb.) definíciója. Ez a "Controller" réteg, ami a HTTP kéréseket fogadja, meghívja a `DataManager` megfelelő metódusait, és `HTTPException` vagy `JSONResponse` segítségével válaszol a kliensnek.

5. **`authentication/authentication.py`**: Az adminisztrátori token-ellenőrzést végző FastAPI függőséget (`verify_token`) tartalmazó modul

6. **`.token`**: A titkos adminisztrátori tokent (egy egyszerű stringet) tartalmazó fájl.