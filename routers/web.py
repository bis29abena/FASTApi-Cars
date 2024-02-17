from fastapi import APIRouter, Request, Depends, Form
from sqlmodel import Session
from db import get_session
from routers.cars import CarRouter
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


class WebRouter(APIRouter):
    def __init__(self):
        super().__init__()
        self.__template = Jinja2Templates(directory="templates")
        self.__cars = CarRouter()

        self.setup_routes()

    def setup_routes(self):
        self.add_api_route(path="/", endpoint=self.home,
                           methods=["GET"], response_class=HTMLResponse)
        self.add_api_route(path="/search", endpoint=self.search,
                           methods=["POST"], response_class=HTMLResponse)

    async def home(self, request: Request):
        """Return an html home page

        Args:
            request (Request): the request of the page

        Returns:
            HTML: HTMLResponse
        """        
        return self.__template.TemplateResponse({"request": request}, "home.html")

    async def search(self, *, size: str = Form(...), doors: int = Form(...),
                     request: Request, session: Session = Depends(get_session)):
        """Take the inputs from a user for a search

        Args:
            request (Request): request data tp serve the html
            size (str, optional): size of the car. Defaults to Form(...).
            doors (int, optional): number of doors of the car. Defaults to Form(...).
            session (Session, optional): session for the db. Defaults to Depends(get_session).

        Returns:
            HTML: HTMLResponse
        """        
        cars = await self.__cars.get_cars(size=size, door=doors, session=session)
        return self.__template.TemplateResponse("search_results.html",
                                                {"request": request, "cars": cars})
