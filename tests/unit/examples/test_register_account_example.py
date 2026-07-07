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
"""Mock-based tests proving `examples/register_account_example.py` works without a server.

The gRPC `Client` (and therefore every network hop) is replaced by a `MagicMock`, so these
tests assert only that the example builds the correct protobuf requests and handles the
`SipStatus` response — no live SIP/CAI backend is required.
"""
import sys
from typing import cast
from unittest import mock
from unittest.mock import MagicMock

import ondewo.sip.sip_pb2 as sip
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig

from examples import register_account_example as ex

# Bound once so a refactor that changes only the example or only the expectation cannot make
# these assertions silently tautological.
EXPECTED_STATUS_TYPE: sip.SipStatus.StatusType.ValueType = sip.SipStatus.READY
EXPECTED_DESCRIPTION: str = 'ready to call'


def _mock_client_returning(status: sip.SipStatus) -> MagicMock:
    """
    Build a `MagicMock` standing in for `Client` whose `get_sip_status` returns `status`.

    Args:
        status (SipStatus):
            The status the mocked `get_sip_status` endpoint should return.

    Returns:
        MagicMock:
            A client mock wired so `services.sip.get_sip_status()` yields `status`.
    """
    client_mock: MagicMock = MagicMock()
    client_mock.services.sip.get_sip_status.return_value = status
    return client_mock


def test_build_config_uses_keycloak_offline_token_path() -> None:
    """`build_config` returns a valid Keycloak-flagged config with no `client_secret`.

    Returns:
        None
    """
    config = ex.build_config()

    assert config.use_keycloak is True
    assert config.user_name == ex.USER_NAME
    assert config.password == ex.PASSWORD
    assert config.client_id == ex.CLIENT_ID
    assert not hasattr(config, 'client_secret')


def test_build_channel_options_declare_retry_policy() -> None:
    """`build_channel_options` embeds a retry policy for the three SIP RPCs.

    Returns:
        None
    """
    options = dict(ex.build_channel_options())

    assert options['grpc.enable_retries'] == 1
    assert 'SipRegisterAccount' in options['grpc.service_config']
    assert 'SipStartSession' in options['grpc.service_config']
    assert 'SipStartCall' in options['grpc.service_config']


def test_run_sip_flow_builds_requests_and_handles_status() -> None:
    """`run_sip_flow` builds the right requests and returns the handled `SipStatus`.

    Returns:
        None
    """
    expected_status = sip.SipStatus(
        status_type=EXPECTED_STATUS_TYPE,
        account_name=ex.ACCOUNT_NAME,
        description=EXPECTED_DESCRIPTION,
    )
    client_mock = _mock_client_returning(expected_status)

    result = ex.run_sip_flow(cast(Client, client_mock))

    sip_service = client_mock.services.sip
    register_request = sip_service.register_account.call_args.kwargs['request']
    assert isinstance(register_request, sip.SipRegisterAccountRequest)
    assert register_request.account_name == ex.ACCOUNT_NAME
    assert register_request.password == ex.ACCOUNT_PASSWORD

    session_request = sip_service.start_session.call_args.kwargs['request']
    assert isinstance(session_request, sip.SipStartSessionRequest)
    assert session_request.account_name == ex.ACCOUNT_NAME

    call_request = sip_service.start_call.call_args.kwargs['request']
    assert isinstance(call_request, sip.SipStartCallRequest)
    assert call_request.callee_id == ex.CALLEE_ADDRESS

    sip_service.get_sip_status.assert_called_once_with()
    assert result is expected_status
    assert result.status_type == EXPECTED_STATUS_TYPE


def test_main_runs_flow_with_mocked_client() -> None:
    """`main` builds a client via the patched `Client` and drives the full flow insecurely.

    Returns:
        None
    """
    expected_status = sip.SipStatus(status_type=EXPECTED_STATUS_TYPE, account_name=ex.ACCOUNT_NAME)

    with mock.patch.object(ex, 'Client') as client_cls, mock.patch.object(sys, 'argv', ['register_account_example']):
        client_cls.return_value = _mock_client_returning(expected_status)
        ex.main()

    client_cls.assert_called_once()
    assert client_cls.call_args.kwargs['use_secure_channel'] is False
    assert isinstance(client_cls.call_args.kwargs['config'], ClientConfig)

    sip_service = client_cls.return_value.services.sip
    sip_service.register_account.assert_called_once()
    sip_service.start_session.assert_called_once()
    sip_service.start_call.assert_called_once()
    sip_service.get_sip_status.assert_called_once_with()
