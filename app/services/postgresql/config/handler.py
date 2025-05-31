import logging

logger = logging.getLogger(__name__)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.postgresql.models.history import Base
import os


class DBConnectionHandler:
    def __init__(self) -> None:
        db_dir = "app/data"
        os.makedirs(db_dir, exist_ok=True)
        self.__connection_string = f"sqlite:///{db_dir}/crypto_history.db"
        self.session = None

    def get_engine(self):
        try:
            engine = create_engine(self.__connection_string)
            Base.metadata.create_all(engine)
            return engine
        except Exception as e:
            logger.error(f"Error creating database engine: {e}")
            raise e

    def __enter__(self):
        try:
            engine = self.get_engine()
            session_maker = sessionmaker()
            self.session = session_maker(bind=engine)
            return self.session
        except Exception as e:
            logger.error(f"Error entering database context: {e}")
            raise e

    def __exit__(self, exc_type, exc_value, trace):
        self.session.close()
