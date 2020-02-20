import hashlib
import datetime
import os
import sys
cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
import api


def set_valid_auth(request):
    if request.get("login") == api.ADMIN_LOGIN:
        msg = datetime.datetime.now().strftime("%Y%m%d%H") + api.ADMIN_SALT
        request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()
    else:
        account = str(request.get("account", ""))
        login = str(request.get("login", ""))
        msg = account + login + api.SALT
        request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()

