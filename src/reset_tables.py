from sqlalchemy import create_engine
from product_scheduler.database.sqlalchemy.models import Base


def init_database():
    engine = create_engine("sqlite:///scheduler.db", echo=True)
    print("initialize tables.")
    Base.metadata.create_all(engine)
    print("finished initialize.")


if __name__ == "__main__":
    init_database()
