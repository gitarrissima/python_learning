from datetime import datetime, date


class LoginEventSerializer1:
    def __init__(self, event):
        self.event = event

    def serialize(self) -> dict:
        return {
            "username": self.event.username,
            "password": "**hidden**",
            "ip": self.event.ip,
            "timestamp": self.event.timestamp.strftime("%Y-%m-%d")
        }


class LoginEvent1:
    SERIALIZER = LoginEventSerializer1

    def __init__(self, username, password, ip, timestamp):
        self.username = username
        self.password = password
        self.ip = ip
        self.timestamp = datetime.strptime(timestamp, '%d.%m.%Y')

    def serialize(self) -> dict:
        return self.SERIALIZER(self).serialize()


def hide_field(field) -> str:
    return "**hidden**"


def format_time(field_timestamp: datetime) -> str:
    return field_timestamp.strftime("%Y-%m-%d")


def show_original(field) -> str:
    return field


class EventSerializer:
    def __init__(self, serialization_fields: dict):
        print('EventSerializer __init__')
        self.serialization_fields = serialization_fields

    def serialize(self, event):
        print('EventSerializer serialize')
        return {
            field: transformation(getattr(event, field))
            for field, transformation in self.serialization_fields.items()
        }


class Serialization:
    def __init__(self, **transformations):
        print('Serialization __init__')
        self.serializer = EventSerializer(transformations)

    def __call__(self, event_class):
        print('Serialization __call__')

        def serialize_method(event_instance):
            print('Serialization __call__ serialize_method')
            return self.serializer.serialize(event_instance)
        event_class.serialize = serialize_method
        return event_class


@Serialization(
    username=show_original,
    password=hide_field,
    ip=show_original,
    timestamp=format_time
)
class LoginEvent:
    def __init__(self, username, password, ip, timestamp):
        self.username = username
        self.password = password
        self.ip = ip
        self.timestamp = datetime.strptime(timestamp, '%d.%m.%Y')


if __name__ == '__main__':
    l1 = LoginEvent1('root', '123456', '1.1.1.1', '11.12.2019')
    print(l1.serialize())


