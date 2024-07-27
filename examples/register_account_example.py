# Copyright 2021-2024 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import json
from typing import (
    Any,
    Set,
    Tuple,
)

import grpc

import ondewo.sip.sip_pb2 as sip
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig

HOST: str = 'localhost'
PORT: str = '1234'
ACCOUNT_NAME: str = 'name@domain.com'
ACCOUNT_PASSWORD: str = 'password'

CALLEE_ADDRESS: str = 'callee'
# TRANSFER_ADDRESS: str = 'transfer'

parser = argparse.ArgumentParser(description="Sip client handling example.")
parser.add_argument("--secure", default=False, action="store_true")
args = parser.parse_args()

# https://github.com/grpc/grpc-proto/blob/master/grpc/service_config/service_config.proto
service_config_json: str = json.dumps(
    {
        "methodConfig": [
            {
                "name": [
                    # To apply retry to all methods, put [{}] as a value in the "name" field
                    # {}
                    # List single rpc method calls
                    {"service": "ondewo.sip.Sip", "method": "SipRegisterAccount"},
                    {"service": "ondewo.sip.Sip", "method": "SipStartSession"},
                    {"service": "ondewo.sip.Sip", "method": "SipStartCall"},
                ],
                "retryPolicy": {
                    "maxAttempts": 10,
                    "initialBackoff": "1.1s",
                    "maxBackoff": "3000s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": [
                        grpc.StatusCode.CANCELLED.name,
                        grpc.StatusCode.UNKNOWN.name,
                        grpc.StatusCode.DEADLINE_EXCEEDED.name,
                        grpc.StatusCode.NOT_FOUND.name,
                        grpc.StatusCode.RESOURCE_EXHAUSTED.name,
                        grpc.StatusCode.ABORTED.name,
                        grpc.StatusCode.INTERNAL.name,
                        grpc.StatusCode.UNAVAILABLE.name,
                        grpc.StatusCode.DATA_LOSS.name,
                    ],
                },
            }
        ]
    }
)

options: Set[Tuple[str, Any]] = {
    # Define custom max message sizes: 1MB here is an arbitrary example.
    ("grpc.max_send_message_length", 1024 * 1024),
    ("grpc.max_receive_message_length", 1024 * 1024),
    # Example of setting KeepAlive options through generic channel_args
    ("grpc.keepalive_time_ms", 2 ** 31 - 1),
    ("grpc.keepalive_timeout_ms", 20000),
    ("grpc.keepalive_permit_without_calls", False),
    ("grpc.http2.max_pings_without_data", 2),
    # Example arg requested for the feature
    ("grpc.dns_enable_srv_queries", 1),
    ("grpc.enable_retries", 1),
    ("grpc.service_config", service_config_json)
}

config = ClientConfig(host=HOST, port=PORT)
client: Client = Client(config=config, use_secure_channel=args.secure, options=options)

request_register: sip.SipRegisterAccountRequest = sip.SipRegisterAccountRequest(
    account_name=ACCOUNT_NAME,
    password=ACCOUNT_PASSWORD,
)
client.services.sip.register_account(request=request_register)

request_start_session: sip.SipStartSessionRequest = sip.SipStartSessionRequest(
    account_name=ACCOUNT_NAME
)
client.services.sip.start_session(request=request_start_session)

request_start_call: sip.SipStartCallRequest = sip.SipStartCallRequest(
    callee_id=CALLEE_ADDRESS
)
client.services.sip.start_call(request=request_start_call)

request = sip.SipTransferCallRequest(
    transfer_id=CALLEE_ADDRESS
)
client.services.sip.transfer_call(request=request)
