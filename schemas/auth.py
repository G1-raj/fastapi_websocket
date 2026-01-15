from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str

    class Config:
        from_attributes = True

class SignUpRespone(BaseModel):
    message: str
    data: UserOut

class LoginResponse(BaseModel):
    message: str
    data: UserOut
    token: TokenResponse

