#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip3 install requests
import requests

url = "https://platform.openmmlab.com/gw/model-inference/openapi/v1/detection"
access_token = "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJyb2wiOiIiLCJqdGkiOiIzZ1E3TU9SM2xJQmdOMFprNjJ3MFlwVkQiLCJpc3MiOiJTbmFpbENsaW1iIiwiaWF0IjoxNjk0NDQ2MzI5LCJzdWIiOiIzZ1E3TU9SM2xJQmdOMFprNjJ3MFlwVkQiLCJleHAiOjE2OTUwNTExMjl9.q-eo7teN_AfF__7K9DlXPA8KbEiFXq7NK3w0Nm-27to_02zPpyb0YDFRFGWgsqF0Ffo6slu6by3ZD_d1Qe6hhw"

body = {
  "resource": "https://oss.openmmlab.com/web-demo/static/one.e9be6cd7.jpg",
  "resourceType": "URL",
  "backend": "PyTorch",
  "requestType": "SYNC",
  "algorithm": "YOLOX"
}

headers = {
  'Authorization': access_token
}


response = requests.post(url, headers=headers, json=body)


print(response.text)