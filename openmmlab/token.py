#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install requests

import hashlib
import random
import time
import requests


def get_nonce():
    pool = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = 10
    ret = ""

    while len(ret) < length:
        ret += random.choice(pool)
    return ret


ts = str(int(time.time()))
nonce = get_nonce()
access_key = "3gQ7MOR3lIBgN0Zk62w0YpVD"
secret_key = "w815AR0k8T1mxjPoM8gYLjz6"

concat_string = "uri=/api/v1/openapi/auth&ts=%s&nonce=%s&accessKey=%s&secretKey=%s" % (ts, nonce, access_key, secret_key)
sign = hashlib.sha256(concat_string.encode("utf-8")).hexdigest()

url = "https://platform.openmmlab.com/gw/user-service/api/v1/openapi/auth"
headers = {
    "ts": ts,
    "nonce": nonce,
    "sign": sign,
    "accessKey": access_key
}
ret = requests.post(url, headers=headers)
print(ret.content)