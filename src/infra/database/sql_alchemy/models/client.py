from sqlalchemy import Column, String

from src.domain.types.entity import Entity
from src.infra.database.sql_alchemy.config import Base
from src.infra.database.sql_alchemy.sql_alchemy_database_model import SQLAlchemyDatabaseModel


class ClientDB(Base, SQLAlchemyDatabaseModel, Entity):
    __tablename__ = "CLIENT"

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
