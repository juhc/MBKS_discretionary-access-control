from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

class AuthInfo(BaseModel):
    username: str 
    access_token: str 
    token_type: str 
    user_id: int