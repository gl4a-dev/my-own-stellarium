from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from core.settings import settings

db_engine = create_engine(settings.get_neonsql_link(), echo=False, future=True)
Base = declarative_base()

if __name__ == "__main__":
    print(db_engine)
    print(Base)