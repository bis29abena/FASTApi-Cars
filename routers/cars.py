from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from routers.user import UserRouter
from db import get_session
from schemas import CarInput, CarOutput, Car, Trip, User

class CarRouter(APIRouter):
    def __init__(self):
        super().__init__(prefix="/api/cars")
        self.setup_routes()

    def setup_routes(self):
        """Set up all the routes in the class
        """        
        self.add_api_route("/", self.get_cars, methods=["GET"])
        self.add_api_route("/{id}", self.car_by_id, methods=["GET"], response_model=CarOutput)
        self.add_api_route("/", self.add_car, methods=["POST"], response_model=Car)
        self.add_api_route("/{id}", self.remove_car, methods=["DELETE"], response_model=None, status_code=204)
        self.add_api_route("/{id}", self.change_car, methods=["PUT"], response_model=Car)
        self.add_api_route("/{car_id}/trips", self.add_trip, methods=["POST"], response_model=Trip)

    async def get_cars(self, size: str | None = None, door: int | None = None, session: Session = Depends(get_session)) -> list:
        """Get a list of cars depending on the size or door

        Args:
            size (str | None, optional): size of the car. Defaults to None.
            door (int | None, optional): size of the door. Defaults to None.
            session (Session, optional): dependency injection for the session. Defaults to Depends(get_session).

        Returns:
            list: return a list of cars
        """        
        query = select(Car)
        if size:
            query = query.where(Car.size == size)
        if door:
            query = query.where(Car.door >= door)
        return session.exec(query).all()

    async def car_by_id(self, id: int, session: Session = Depends(get_session)) -> CarOutput:
        """Get a car by an ID

        Args:
            id (int): Id of the car
            session (Session, optional): session. Defaults to Depends(get_session).

        Raises:
            HTTPException: Raise a 404 reponse when there is no car found

        Returns:
            CarOutput: Return a car object when a car is foung
        """        
        car = session.get(Car, id)
        if car:
            return car
        else:
            raise HTTPException(status_code=404, detail="No car was found") 

    async def add_car(self, car_input: CarInput, session: Session = Depends(get_session),
                      user: User = Depends(UserRouter.get_current_user)) -> Car:
        """Add a Car object to the car table

        Args:
            car_input (CarInput): car input object to be added to the table
            session (Session, optional): session. Defaults to Depends(get_session).

        Returns:
            Car: Return the car object when is created
        """        
        new_car = Car.from_orm(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car)
        return new_car

    async def remove_car(self, id: int, session: Session = Depends(get_session)) -> None:
        """Remove a car from the table by an id

        Args:
            id (int): parameter ID
            session (Session, optional): _description_. Defaults to Depends(get_session).

        Raises:
            HTTPException: Raise a 404 not found exception when no car was found
        """        
        car = session.get(Car, id)
        if car:
            session.delete(car)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"No car with id={id}")

    async def change_car(self, id: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
        """Change the details of car which already exist

        Args:
            id (int): ID of the car to changer
            new_data (CarInput): New Car Data
            session (Session, optional): _description_. Defaults to Depends(get_session).

        Raises:
            HTTPException: Raise a 404 not found error if there is no car found by the id

        Returns:
            Car: Return when the car data is changed
        """        
        car = session.get(Car, id)
        if car:
            car.fuel = new_data.fuel
            car.transmission = new_data.transmission
            car.door = new_data.door
            car.size = new_data.size
            session.commit()
            return car
        else:
            raise HTTPException(status_code=404, detail=f"No car with id={id}")

    async def add_trip(self, car_id: int, trip_input: Trip, session: Session = Depends(get_session)) -> Trip:
        """Add a trip to a car

        Args:
            car_id (int): car_id 
            trip_input (Trip): trip_input_data
            session (Session, optional): session. Defaults to Depends(get_session).

        Raises:
            HTTPException: Raise a 404 not found errror when there is no car to be found

        Returns:
            Trip: Return a trip when is created
        """        
        car = session.get(Car, car_id)
        if car:
            trip_input.car_id = car_id
            new_trip = Trip.from_orm(trip_input)
            car.trips.append(new_trip)
            session.commit()
            session.refresh(new_trip)
            return new_trip
        else:
            raise HTTPException(status_code=404, detail=f"No car with id={car_id}")

