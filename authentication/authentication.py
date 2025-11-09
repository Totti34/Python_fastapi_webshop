from fastapi import Header, HTTPException, status

def get_token_from_file():
    with open("authentication/.token", "r") as f:
        return f.read().strip()

def verify_token(token: str = Header(..., alias="Token")):
    stored_token = get_token_from_file()
    if token != stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="A megadott Token nem megfelelő!"
        )