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

from ondewo.sip.client.client_config import ClientConfig
from ondewo.sip.client.client import Client

import ondewo.sip.sip_pb2 as sip

with open('sip_config.json') as fi:
    config = ClientConfig.from_json(fi.read())

client = Client(config=config, use_secure_channel=False)

request = sip.RegisterAccountRequest(
    account_name='example@aim.ondewo.com',
    password='asdfasdfasdfasdfasfdasfsdf',
)
client.services.sip.register_account(request=request)

request = sip.StartSessionRequest(
    account='example'
)
client.services.sip.start_session(request=request)

request = sip.StartCallRequest(
    callee_id='0043123123123'
)
client.services.sip.start_call(request=request)
