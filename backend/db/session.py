from sqlalchemy.orm import sessionmaker

from db.connection import db_engine

def get_session():
    try:
        Session = sessionmaker(bind=db_engine)
        session = Session()
        yield session
    finally:
        session.close()

if __name__ == "__main__":
    print(get_session())