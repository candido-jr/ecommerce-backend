from app.db.base import Base
from app.db.session import engine


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
