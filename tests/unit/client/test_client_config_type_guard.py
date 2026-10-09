# Copyright 2021-2026 ONDEWO GmbH
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
"""Both clients reject a config that is not an `ondewo.sip` `ClientConfig`.

`_initialize_services` takes the `BaseClientConfig` the base class declares and narrows it with an
`isinstance` guard (as ondewo-nlu-client-python does) instead of a `type: ignore`. `client.py` and
`async_client.py` carry independent copies of the guard, so each has its own test.
"""

import asyncio
import re

import pytest
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.sip.client.async_client import AsyncClient
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig

HOST: str = "localhost"
PORT: str = "50055"
CONFIG_TYPE_ERROR_MESSAGE: str = "The provided config must be of type `ondewo.sip.client.client_config.ClientConfig`"


def _sip_config() -> ClientConfig:
    """Build the smallest valid SIP `ClientConfig` (`user_name` and `password` are mandatory)."""
    return ClientConfig(host=HOST, port=PORT, user_name="tech-user@example.com", password="s3cr3t")


def test_client_rejects_a_base_config() -> None:
    """Passing the generic `BaseClientConfig` to `Client` raises `ValueError`."""
    with pytest.raises(ValueError, match=re.escape(CONFIG_TYPE_ERROR_MESSAGE)):
        Client(config=BaseClientConfig(host=HOST, port=PORT), use_secure_channel=False)


def test_async_client_rejects_a_base_config() -> None:
    """Passing the generic `BaseClientConfig` to `AsyncClient` raises `ValueError` before any channel is built."""
    with pytest.raises(ValueError, match=re.escape(CONFIG_TYPE_ERROR_MESSAGE)):
        AsyncClient(config=BaseClientConfig(host=HOST, port=PORT), use_secure_channel=False)


def test_client_accepts_its_own_config() -> None:
    """A `sip` `ClientConfig` passes the guard and wires the services."""
    client: Client = Client(config=_sip_config(), use_secure_channel=False)
    assert client.services.sip is not None
    client.disconnect()


def test_async_client_accepts_its_own_config() -> None:
    """A `sip` `ClientConfig` passes the async guard and wires the services (built inside a running loop)."""

    async def _build_and_close() -> None:
        client: AsyncClient = AsyncClient(config=_sip_config(), use_secure_channel=False)
        assert client.services.sip is not None
        await client.disconnect()

    asyncio.run(_build_and_close())
