import os

from sqlmodel import create_engine, SQLModel, Session


DB_HOST = os.environ.get('compose_db_name')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')

print(DB_HOST, flush=True)



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    print('####################################')
    with Session(engine) as session:
        return session