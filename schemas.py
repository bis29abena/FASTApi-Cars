# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR
from typing import Optional
from passlib.context import CryptContext
# import json

pwd_context = CryptContext(schemes=["bcrypt"])

class TripInput(SQLModel):
    start: int
    end: int
    description: str
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "start": 5,
                "end": 6,
                "description": "miles"
            }
        }
        
class TripOutput(TripInput):
    id: int

class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    door: int
    transmission: str | None = "auto"
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "size": "m",
                "fuel": "hybrid",
                "door": 4,
                "transmission": "auto"
            }
        }
    
class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []
    

    
class Trip(TripInput, table=True):
    id: Optional[int] = Field(default= None, primary_key=True)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")
    
class Car(CarInput, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")
    

class UserInput(SQLModel):
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""
    
    class ConfigDict:
        json_schema_extra = {
            "example": {
                "username": "bosei",
                "password_hash": "jbqducuycu"
            }
        }
        
class UserOutput(SQLModel):
    id: int
    username: str

class User(UserInput, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    

# def load_db() -> list[CarOutput]:
#     """Open a CarInputs.json file

#     Returns:
#         list[CarInput]: Return a list of CarInput object
#     """    
#     with open("cars.json") as f:
#         return [CarOutput.parse_obj(obj) for obj in json.load(f)]
    
# def save_db(car: list[CarOutput]) -> None:
#     """Save a list of CarInputs

#     Args:
#         CarInputs (list[CarInput]): Takes a list of CarInputs
#     """    
#     with open("cars.json", "w") as f:
#         json.dump([CarInput.dict() for CarInput in car], f, indent=4)