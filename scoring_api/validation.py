import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Validation:

    def __init__(self, validation_function):
        self.validation_function = validation_function

    def __call__(self, arg_name, value) -> bool:
        return self.validation_function(arg_name, value)

    @staticmethod
    def validate_string(arg_name: str, value) -> bool:
        """
            This function checks that value is string
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if not isinstance(value, str):
            raise ValueError(f"Parameter '{arg_name}' expected to be string. Actual type is {type(value)}")

        return True

    @staticmethod
    def validate_date(arg_name: str, value) -> bool:
        """
            This function checks that value is string
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: datetime object if validation passed. Otherwise exception
        """

        if value is None:
            return True

        datetime.strptime(value, '%d.%m.%Y')
        return True

    @staticmethod
    def validate_arguments(arg_name: str, value) -> bool:
        """
            This function checks 'argument' field
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if not isinstance(value, dict):
            raise ValueError(f"Parameter '{arg_name}' expected to be dict. Actual type is {type(value)}")

        return True

    @staticmethod
    def validate_phone_number(arg_name: str, value) -> bool:
        """
            This function validates input value as phone number
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if not isinstance(value, int) and not isinstance(value, str):
            raise ValueError(f"Parameter '{arg_name}' should be 'int' or 'str'. Actual type is {type(value)}")

        if isinstance(value, int):
            value = str(value)

        r = re.compile(r'^7\d{10}$')
        if isinstance(value, str) and not r.match(value):
            raise ValueError(
                f"Parameter '{arg_name}' should contain 11 numeric symbols and start with '7'. "
                f"Actual length is {len(value)}, first symbol is '8'")

        return True

    @staticmethod
    def validate_email(arg_name: str, value) -> bool:
        """
            This function validates input value as email
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if not isinstance(value, str):
            raise ValueError(f"Parameter '{arg_name}' should be 'str'. Actual type is {type(value)}")

        if '@' not in value:
            raise ValueError(f"Parameter '{arg_name}' should contain '@'")

        chunks = value.split('@')
        r = re.compile(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
        if not r.match(chunks[1]):
            raise ValueError(f"Parameter '{arg_name}' contains invalid domain part: chunks[1]")

        return True

    @staticmethod
    def validate_birthday(arg_name: str, value) -> bool:
        """
            This function validates input value as birthday
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        datetime_value = datetime.strptime(value, '%d.%m.%Y')
        seventy_years_ago = datetime.today() - timedelta(days=70 * 365 - 17)
        if datetime_value < seventy_years_ago:
            raise ValueError(f"Parameter '{arg_name}' provided expected to be less than 70 years ago")

        return True

    @staticmethod
    def validate_gender(arg_name: str, value) -> bool:
        """
            This function validates input value as gender
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if value not in (0, 1, 2):
            raise ValueError(f"Parameter '{arg_name}' expected to be in set (1, 2, 3)")

        return True

    @staticmethod
    def validate_client_ids(arg_name: str, value) -> bool:
        """
            This function validates input value as clients_ids
            :param arg_name: name of argument to check (just for clear error message)
            :param value: value to check
            :return: True if validation passed. Otherwise exception
        """

        if value is None:
            return True

        if not isinstance(value, list):
            raise ValueError(f"Parameter '{arg_name}' should be 'list'. Actual type is {type(value)}")

        if len(value) == 0:
            raise ValueError(f"Parameter '{arg_name}' should be not empty list")

        for client_id in value:
            if not isinstance(client_id, int):
                raise ValueError(
                    f"Parameter '{arg_name}' should contain only 'int' elements, but it contains '{client_id}', "
                    f"which type is {type(value)}")

        return True
