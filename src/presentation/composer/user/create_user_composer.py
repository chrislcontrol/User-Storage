from src.domain.use_cases.user.create_user_use_case import CreateUserUseCase
from src.infra.adapters.bcrypt_adapter import BcryptAdapter
from src.infra.database.db_connection_handler import DBHandler
from src.infra.repositories.postgres.postgres_user_repository import PostgresUserRepository
from src.presentation.controllers.user.create_user_controller import CreateUserController


def create_user_composer(db: DBHandler) -> CreateUserController:
    user_repository = PostgresUserRepository(db=db)
    encryptor = BcryptAdapter()
    create_user_use_case = CreateUserUseCase(user_repository=user_repository, encryptor=encryptor)
    return CreateUserController(create_user_use_case=create_user_use_case)
