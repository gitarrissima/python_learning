import logging
from .validation import Validation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DataField:

    def __init__(self, required: bool, nullable: bool, validation: Validation = None):
        logger.info('DataField __init__')
        self._name = None
        self._required = required
        self._nullable = nullable
        self._validation = validation

    def __set_name__(self, owner, name):
        logger.info('DataField __set_name__')
        self._name = name

    def __get__(self, instance, owner):
        logger.info('DataField __get__')
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
        logger.info('DataField __set__')
        self._validate(value)
        instance.__dict__[self._name] = value


class CharField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_string(name, value)))


class EmailField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_email(name, value)))


class PhoneField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_phone_number(name, value)))


class BirthDayField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_birthday(name, value)))


class GenderField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_gender(name, value)))


class OnlineScoreRequest:
    first_name = CharField(required=True, nullable=False)
    last_name = CharField(required=True, nullable=False)
    email = EmailField(required=True, nullable=False)
    phone = PhoneField(required=True, nullable=False)
    birthday = BirthDayField(required=True, nullable=False)
    gender = GenderField(required=True, nullable=False)

    def __init__(self, arguments: dict):
        self.first_name = arguments['first_name'] if 'first_name' in arguments else None
        self.last_name = arguments['last_name'] if 'last_name' in arguments else None
        self.email = arguments['email'] if 'email' in arguments else None
        self.phone = arguments['phone'] if 'phone' in arguments else None
        self.birthday = arguments['birthday'] if 'birthday' in arguments else None
        self.gender = arguments['gender'] if 'gender' in arguments else None
