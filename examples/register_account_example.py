#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2021 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ondewo.sip.sip_pb2 as sip
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig

HOST: str = 'localhost'
PORT: int = 0
ACCOUNT_NAME: str = 'name@domain.com'
ACCOUNT_PASSWORD: str = 'password'

CALLEE_ADDRESS: str = 'callee'
# TRANSFER_ADDRESS: str = 'transfer'

# with open('sip_config.json') as fi:
#     config = ClientConfig.from_json(fi.read())

config = ClientConfig(host=HOST, port=PORT)
client = Client(config=config, use_secure_channel=False)

request_register: sip.RegisterAccountRequest = sip.RegisterAccountRequest(
    account_name=ACCOUNT_NAME,
    password=ACCOUNT_PASSWORD,
)
client.services.sip.register_account(request=request_register)

request_start_session: sip.StartSessionRequest = sip.StartSessionRequest(
    account_name=ACCOUNT_NAME
)
client.services.sip.start_session(request=request_start_session)

request_start_call: sip.StartCallRequest = sip.StartCallRequest(
    callee_id=CALLEE_ADDRESS
)
client.services.sip.start_call(request=request_start_call)

# request = sip.TransferCallRequest(
#     transfer_id=TRANSFER_ADDRESS
# )
# client.services.sip.transfer_call(request=request)
