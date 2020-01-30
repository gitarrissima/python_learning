import logging
from validation import Validation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DataField:

    def __init__(self, required: bool, nullable: bool, validation: Validation = None):
        self._name = None
        self._required = required
        self._nullable = nullable
        self._validation = validation

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def _validate(self, value) -> bool:
        """
            This function implements validation of value before set
            :param value:
            :return: True if validation passed, raise exception if not
        """

        if self._required and value is None:
            raise ValueError(f"Required parameter '{self._name}' should be defined")

        if not self._nullable and value == '':
            raise ValueError(f"Parameter '{self._name}' should not be empty")

        self._validation(self._name, value)

    def __set__(self, instance, value):
        self._validate(value)
        instance.__dict__[self._name] = value
