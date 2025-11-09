from fastapi import Header, HTTPException, status



"""
A jelenlegi fájl az alkalmazás hitelesítési (authentication) logikáját
tartalmazza.

A 'verify_token' függvény egy FastAPI Függőség (Dependency),
amely a feladatkiírásnak megfelelően az adminisztrátori végpontok 
védelmére szolgál egy "egyszerű string" alapú ellenőrzéssel.

A 'get_token_from_file' beolvassa a titkos tokent
a '.token' fájlból. A 'verify_token' ezt összehasonlítja a kliens által
a 'Token' header-ben küldött értékkel.

Ha a két token nem egyezik, a függvény 'HTTPException'-t
dob (401 Unauthorized),
még mielőtt a védett végpont logikája lefutna.
"""



def get_token_from_file():
    with open("authentication/.token", "r") as f:
        return f.read().strip()

def verify_token(token: str = Header(..., alias="Token")):
    stored_token = get_token_from_file()
    if token != stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="A megadott Token nem megfelelő!")