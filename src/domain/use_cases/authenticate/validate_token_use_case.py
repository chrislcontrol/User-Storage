from typing import Dict, Union

from src.domain.entities.client import Client
from src.domain.entities.token import Token
from src.domain.exceptions.invalid_credentials import InvalidCredentials
from src.domain.repositories.token_repository import TokenRepository
from src.domain.types.token import AuthorizationToken
from src.domain.types.use_case import UseCase


class ValidateTokenUseCase(UseCase):
    def __init__(self, *, token_repository: TokenRepository):
        self._token_repository = token_repository

    def validate(self, *, token_string: AuthorizationToken) -> Dict[str, Union[Token, Client, bool]]:
        token = self._token_repository.get_token_by_string(token=token_string.without_prefix())
        if not token:
            raise InvalidCredentials()
        return {
            "token": token,
            "client": token.client,
            "success": bool(token)
        }
