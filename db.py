from sqlmodel import create_engine, Session


engine = create_engine(
    url="sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},
    echo=True
)


async def get_session():
    with Session(engine) as session:
        yield session
        