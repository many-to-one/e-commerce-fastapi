from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional



class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int


class ChangePasswordForm(BaseModel):
    # email: EmailStr
    old_password: str
    new_password: str