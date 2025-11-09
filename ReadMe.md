Az alkalmazás architektúrája:

1. **`main.py`**: A fő FastAPI alkalmazásfájl. Ez indítja el az Uvicorn szervert és tölti be a `routers/routes.py`-ban definiált végpontokat.
- [cite_start]**`.token`**: (Gitignore-ban kellene lennie) A titkos adminisztrátori tokent (egy egyszerű stringet) tartalmazó fájl.

2. **`ReadMe.md`**: Ez a dokumentáció.

3. **`schemas/schema.py`**: A Pydantic adatmodellek (`User`, `Item`, `Basket`) definíciója. Ez a réteg felel az adatok validálásáért is (pl. hogy az ID-k pozitívak, az e-mail címek érvényesek)

4. **`data/datamanager.py`**: A központi adatkezelő osztály (`DataManager`). Ez a "Service" réteg felel minden fájlműveletért (JSON olvasás/írás) és az üzleti logikáért. Kommunikál a `users.json` és `data.json` fájlokkal.

5. **`routers/routes.py`**: Az összes API végpont (`@routers.get`, `@routers.post` stb.) definíciója. [cite_start]Ez a "Controller" réteg, ami a HTTP kéréseket fogadja, meghívja a `DataManager` megfelelő metódusait, és `HTTPException` vagy `JSONResponse` segítségével válaszol a kliensnek.
6. **`authentication/authentication.py`**: Az adminisztrátori token-ellenőrzést végző FastAPI függőséget (`verify_token`) tartalmazó modul
