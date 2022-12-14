from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.presentation.base.schema.base_field_protocol import BaseFieldProtocol


class SuccessMessage(Enum):
    SUCCESS = 'SUCCESS'


class FailReason(Enum):
    REQUIRED_FIELD = 'REQUIRED_FIELD'
    INVALID_TYPE = 'INVALID_TYPE'
    MIN_LENGHT = 'MIN_LENGHT'
    MAX_LENGHT = 'MAX_LENGHT'
    UNKNOW = 'UNKNOW'


@dataclass
class BaseField(BaseFieldProtocol):
    type: type
    default: Any = None
    min_lenght: int = None
    max_length: int = None
    required: bool = True

    def __post_init__(self):
        if self.default in [{}, [], ()]:
            raise ValueError(r'Default value should not be {}, [] or (). Might be dict, list or tuple instead.')

        if self.default is not None and self.required is True:
            self.required = False

        self.default = {dict: {}, list: [], tuple: ()}.get(self.default, self.default)

    def validate(self, value: any) -> (bool, FailReason):
        if self.__is_null_or_blank(value) and self.required:
            return self._fail(FailReason.REQUIRED_FIELD)

        elif self.__is_null_or_blank(value) and not self.required:
            return self._success()

        if not isinstance(value, self.type):
            return self._fail(FailReason.INVALID_TYPE)

        try:
            if self.min_lenght and len(value) < self.min_lenght:
                return self._fail(FailReason.MIN_LENGHT)

            if self.max_length and len(value) > self.max_length:
                return self._fail(FailReason.MAX_LENGHT)

        except TypeError:
            pass

        return self._success()

    def _fail(self, message: FailReason) -> (bool, FailReason):
        return False, message

    def _success(self, message: SuccessMessage = SuccessMessage.SUCCESS) -> (bool, SuccessMessage):
        return True, message

    def __is_null_or_blank(self, value):
        return not value or value == ""
