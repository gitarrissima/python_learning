import json
import datetime
import logging
import hashlib
import uuid
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from scoring import *
from validation import Validation
from data_field import DataField

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class ArgumentsField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_arguments(name, value)))


class DateField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_date(name, value)))


class ClientIDsField(DataField):
    def __init__(self, required: bool = False, nullable: bool = True):
        super().__init__(required, nullable,
                         validation=Validation(lambda name, value: Validation.validate_client_ids(name, value)))


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


class ClientsInterestsRequest(object):
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)

    def __init__(self, arguments: dict):
        self.client_ids = arguments['client_ids'] if 'client_ids' in arguments else None
        self.date = arguments['date'] if 'date' in arguments else None


class OnlineScoreRequest(object):
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def __init__(self, arguments: dict):
        self.first_name = arguments['first_name'] if 'first_name' in arguments else None
        self.last_name = arguments['last_name'] if 'last_name' in arguments else None
        self.email = arguments['email'] if 'email' in arguments else None
        self.phone = arguments['phone'] if 'phone' in arguments else None
        self.birthday = arguments['birthday'] if 'birthday' in arguments else None
        self.gender = arguments['gender'] if 'gender' in arguments else None

        if not self.check_attribute_pairs():
            raise ValueError(
                "At least one pair should be defined with not None values: " +
                "phone-email, first_name-last_name, gender-birthday")

    def get_not_empty_fields(self) -> list:
        """
        This function returns list of object attributes which are not empty
        :return: list of attribute names which values are not None.
        """

        not_empty_fields = list()
        all_fields = vars(self).items()

        for field, value in all_fields:
            if getattr(self, field) is not None:
                not_empty_fields.append(field)

        return not_empty_fields

    def check_attribute_pairs(self) -> bool:
        """
        This function implements extra validation for object.
        Check if there is at least one not None pair defined:
        - phone-email
        - first name-last name
        - gender-birthday
        :return: True if conditions are met
        """

        if self.phone is not None and self.email is not None:
            return True

        if self.first_name is not None and self.last_name is not None:
            return True

        if self.gender is not None and self.birthday is not None:
            return True

        return False


class MethodRequest(object):
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    def __init__(self, arguments: dict):
        self.account = arguments['account'] if 'account' in arguments else None
        self.login = arguments['login'] if 'login' in arguments else None
        self.token = arguments['token'] if 'token' in arguments else None
        self.arguments = arguments['arguments'] if 'arguments' in arguments else None
        self.method = arguments['method'] if 'method' in arguments else None

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def check_auth(request):
    if request.is_admin:
        s = (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode('utf-8')
        digest = hashlib.sha512(s).hexdigest()
    else:
        s = (request.account + request.login + SALT).encode('utf-8')
        digest = hashlib.sha512(s).hexdigest()
    if digest == request.token:
        return True
    return False


def online_score_handler(request, ctx, store):
    print(f"Request = {request}")
    try:
        method_request = MethodRequest(request['body'])
        if not check_auth(method_request):
            return {"error": "Forbidden"}, 403
        if method_request.is_admin:
            return {"score": 42}, 200
    except Exception as e:
        print(e)
        return str(e), 422

    try:
        online_score_params = OnlineScoreRequest(request['body']['arguments'])
    except Exception as e:
        print(e)
        return str(e), 422

    ctx['has'] = online_score_params.get_not_empty_fields()

    score = get_score(phone=getattr(online_score_params, 'phone'),
                      email=getattr(online_score_params, 'email'),
                      birthday=getattr(online_score_params, 'birthday'),
                      gender=getattr(online_score_params, 'gender'),
                      first_name=getattr(online_score_params, 'first_name'),
                      last_name=getattr(online_score_params, 'last_name'))

    print(f"Score = {score}")
    return {"score": score}, 200


def clients_interests_handler(request, ctx, store):
    print(f"Request interests = {request}")
    try:
        client_interests_params = ClientsInterestsRequest(request['body']['arguments'])
    except Exception as e:
        print(e)
        return str(e), 422

    result = dict()
    for cid in client_interests_params.client_ids:
        result[cid] = get_interests(store, cid)

    ctx['nclients'] = len(client_interests_params.client_ids)
    print(f"Result = {result}")
    return result, 200


def method_handler(request, ctx, store):
    response, code = None, None
    if 'method' not in request['body']:
        return "'method' not found in request", 422

    if request and request['body'] and request['body']['method']:
        method = request['body']['method']
        if method == 'online_score':
            response, code = online_score_handler(request, ctx, store)
        if method == 'clients_interests':
            response, code = clients_interests_handler(request, ctx, store)
    else:
        # TODO
        pass
    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "method": method_handler
    }
    store = None

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r))
        return


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default=None)
    (opts, args) = op.parse_args()
    logging.basicConfig(filename=opts.log, level=logging.INFO,
                        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
