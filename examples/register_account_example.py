# Copyright 2021-2025 ONDEWO GmbH
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
"""Minimal end-to-end example for the ONDEWO SIP Python client.

It builds a :class:`ClientConfig`, constructs a :class:`Client`, registers a SIP account,
starts a session, places a call, and reads the resulting :class:`SipStatus`.

Authentication follows the client's current convention: the Keycloak headless
offline-token flow (D18). Set ``keycloak_url``, ``realm``, and ``client_id`` together with
``user_name``/``password`` to use it. Leaving the three Keycloak fields empty attaches no
auth token (``user_name``/``password`` are always required).

Run it directly against a deployment::

    python -m examples.register_account_example            # insecure channel
    python -m examples.register_account_example --secure   # TLS channel
"""
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

# Connection + SDK technical-user credentials (replace with your deployment's values).
HOST: str = 'localhost'
PORT: str = '1234'
USER_NAME: str = 'tech-user@example.com'
PASSWORD: str = 'secret'

# Keycloak headless offline-token auth (D18). The public SDK client carries no secret.
# Leave the three fields empty to attach no auth token.
KEYCLOAK_URL: str = 'https://my-host/auth'
REALM: str = 'ondewo-ccai-platform'
CLIENT_ID: str = 'ondewo-sip-cai-sdk-public'

# SIP account to register and the address to place a call to.
ACCOUNT_NAME: str = 'name@domain.com'
ACCOUNT_PASSWORD: str = 'password'
CALLEE_ADDRESS: str = 'callee'


def build_channel_options() -> Set[Tuple[str, Any]]:
    """
    Build the gRPC channel options, including a per-method retry policy.

    Returns:
        Set[Tuple[str, Any]]:
            Channel options passed straight to the gRPC channel constructor.
    """
    # https://github.com/grpc/grpc-proto/blob/master/grpc/service_config/service_config.proto
    service_config_json: str = json.dumps(
        {
            'methodConfig': [
                {
                    'name': [
                        {'service': 'ondewo.sip.Sip', 'method': 'SipRegisterAccount'},
                        {'service': 'ondewo.sip.Sip', 'method': 'SipStartSession'},
                        {'service': 'ondewo.sip.Sip', 'method': 'SipStartCall'},
                    ],
                    'retryPolicy': {
                        'maxAttempts': 10,
                        'initialBackoff': '1.1s',
                        'maxBackoff': '3000s',
                        'backoffMultiplier': 2,
                        'retryableStatusCodes': [
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
        ('grpc.max_send_message_length', 1024 * 1024),
        ('grpc.max_receive_message_length', 1024 * 1024),
        ('grpc.keepalive_time_ms', 2 ** 31 - 1),
        ('grpc.keepalive_timeout_ms', 20000),
        ('grpc.keepalive_permit_without_calls', False),
        ('grpc.http2.max_pings_without_data', 2),
        ('grpc.dns_enable_srv_queries', 1),
        ('grpc.enable_retries', 1),
        ('grpc.service_config', service_config_json),
    }
    return options


def build_config() -> ClientConfig:
    """
    Build the client configuration for the Keycloak offline-token auth path.

    Returns:
        ClientConfig:
            A validated configuration whose `use_keycloak` flag is True.
    """
    return ClientConfig(
        host=HOST,
        port=PORT,
        user_name=USER_NAME,
        password=PASSWORD,
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
    )


def build_client(config: ClientConfig, use_secure_channel: bool) -> Client:
    """
    Construct the SIP client from a configuration.

    Args:
        config (ClientConfig):
            The validated client configuration.
        use_secure_channel (bool):
            Whether to open a TLS gRPC channel (requires `grpc_cert` on the config).

    Returns:
        Client:
            A ready-to-use SIP client.
    """
    return Client(
        config=config,
        use_secure_channel=use_secure_channel,
        options=build_channel_options(),
    )


def run_sip_flow(client: Client) -> sip.SipStatus:
    """
    Register an account, start a session, place a call, and read the SIP status.

    Args:
        client (Client):
            The SIP client whose `services.sip` endpoints are called.

    Returns:
        SipStatus:
            The status returned by `get_sip_status`, after handling.
    """
    client.services.sip.register_account(
        request=sip.SipRegisterAccountRequest(account_name=ACCOUNT_NAME, password=ACCOUNT_PASSWORD),
    )
    client.services.sip.start_session(
        request=sip.SipStartSessionRequest(account_name=ACCOUNT_NAME),
    )
    client.services.sip.start_call(
        request=sip.SipStartCallRequest(callee_id=CALLEE_ADDRESS),
    )

    status: sip.SipStatus = client.services.sip.get_sip_status()
    status_name: str = sip.SipStatus.StatusType.Name(status.status_type)
    print(f'SIP status: {status_name} (account={status.account_name!r}) — {status.description}')
    return status


def main() -> None:
    """Parse CLI args, build the client, and run the representative SIP flow."""
    parser = argparse.ArgumentParser(description='Sip client handling example.')
    parser.add_argument('--secure', default=False, action='store_true')
    args = parser.parse_args()

    config: ClientConfig = build_config()
    client: Client = build_client(config=config, use_secure_channel=args.secure)
    run_sip_flow(client=client)


if __name__ == '__main__':
    main()
