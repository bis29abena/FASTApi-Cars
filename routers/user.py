from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select, Session
from starlette import status

from db import get_session
from schemas import UserOutput, User

URL_PREFIX = "/auth"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URL_PREFIX}/token")

class UserRouter(APIRouter):
    def __init__(self):
        super().__init__(prefix=URL_PREFIX)
        self.setup_routes()
        
    def setup_routes(self):
        self.add_api_route("/token", self.login, methods=["POST"])
    
    @classmethod    
    def get_current_user(cls, token: str = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)) -> UserOutput:
        query = select(User).where(User.username == token)
        user = session.exec(query).first()
        
        if user:
            return UserOutput.from_orm(user)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username and password",
                                headers={"WWW-Authenticate": "Bearer"})
            
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(get_session)):
        query = select(User).where(User.username == form_data.username)
        user = session.exec(query).first()
        
        if user and user.verify_password(form_data.password):
            return {"access_token": user.username, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrest username and password")
        
        