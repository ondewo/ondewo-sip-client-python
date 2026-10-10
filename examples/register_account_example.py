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

Configuration is read from ``examples/environment.env`` (loaded via python-dotenv), so no
values are hardcoded. Copy that template and fill in your deployment's values.

Run it directly against a deployment::

    python -m examples.register_account_example            # insecure channel
    python -m examples.register_account_example --secure   # TLS channel
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import grpc
from dotenv import load_dotenv
from loguru import logger as log

import ondewo.sip.sip_pb2 as sip
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig

# Load the canonical env-var template next to this script so `cwd` does not matter.
load_dotenv(Path(__file__).with_name("environment.env"))


def _env_flag(name: str, default: str = "false") -> bool:
    """
    Read a boolean-ish environment variable.

    Args:
        name (str):
            The environment variable name.
        default (str):
            The value to assume when the variable is unset.

    Returns:
        bool:
            True when the value is one of 'true', '1', 'yes' (case-insensitive).
    """
    return os.getenv(name, default).strip().lower() in ("true", "1", "yes")


# Connection + SDK technical-user credentials (from examples/environment.env).
HOST: str = os.environ["ONDEWO_HOST"]
PORT: str = os.environ["ONDEWO_PORT"]
USER_NAME: str = os.environ["ONDEWO_USER_NAME"]
PASSWORD: str = os.environ["ONDEWO_PASSWORD"]
USE_SECURE_CHANNEL: bool = _env_flag("ONDEWO_USE_SECURE_CHANNEL")
# Paths to PEM files (the config takes their CONTENT): the CA to trust and, for mutual TLS,
# the client certificate and its private key (set both or neither).
GRPC_CERT_PATH: str = os.getenv("ONDEWO_GRPC_CERT", "")
GRPC_CLIENT_CERT_PATH: str = os.getenv("ONDEWO_GRPC_CLIENT_CERT", "")
GRPC_CLIENT_KEY_PATH: str = os.getenv("ONDEWO_GRPC_CLIENT_KEY", "")

# Keycloak headless offline-token auth (D18). The public SDK client carries no secret.
# Leave the three fields empty to attach no auth token.
KEYCLOAK_URL: str = os.getenv("KEYCLOAK_URL", "")
REALM: str = os.getenv("KEYCLOAK_REALM", "")
CLIENT_ID: str = os.getenv("KEYCLOAK_CLIENT_ID", "")

# SIP account to register and the address to place a call to.
ACCOUNT_NAME: str = os.environ["ONDEWO_SIP_ACCOUNT_NAME"]
ACCOUNT_PASSWORD: str = os.environ["ONDEWO_SIP_ACCOUNT_PASSWORD"]
CALLEE_ADDRESS: str = os.environ["ONDEWO_SIP_CALLEE_ADDRESS"]


def read_pem(path: str) -> Optional[str]:
    """
    Read a PEM file's content, the form ``ClientConfig`` takes for certificates and keys.

    Args:
        path (str):
            Path to the PEM file, or an empty string when it is not configured.

    Returns:
        Optional[str]:
            The file content, or ``None`` when ``path`` is empty.
    """
    return Path(path).read_text() if path else None


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
        grpc_cert=read_pem(GRPC_CERT_PATH),
        grpc_client_cert=read_pem(GRPC_CLIENT_CERT_PATH),
        grpc_client_key=read_pem(GRPC_CLIENT_KEY_PATH),
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
            Whether to open a TLS gRPC channel (requires `grpc_cert` on the config; a client
            certificate and key on the config make it mutual TLS).

    Returns:
        Client:
            A ready-to-use SIP client.
    """
    # No custom channel options: the client's defaults retry only idempotent methods, so a
    # SipRegisterAccount / SipStartSession / SipStartCall is never sent twice.
    return Client(config=config, use_secure_channel=use_secure_channel)


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
    log.info("START: register_account_example: run_sip_flow")
    try:
        log.info(f"Registering SIP account account_name={ACCOUNT_NAME!r}")
        client.services.sip.register_account(
            request=sip.SipRegisterAccountRequest(account_name=ACCOUNT_NAME, password=ACCOUNT_PASSWORD),
        )
        log.info(f"Starting SIP session account_name={ACCOUNT_NAME!r}")
        client.services.sip.start_session(
            request=sip.SipStartSessionRequest(account_name=ACCOUNT_NAME),
        )
        log.info(f"Placing SIP call callee_id={CALLEE_ADDRESS!r}")
        client.services.sip.start_call(
            request=sip.SipStartCallRequest(callee_id=CALLEE_ADDRESS),
        )

        status: sip.SipStatus = client.services.sip.get_sip_status()
    except grpc.RpcError as rpc_error:
        log.error(f"gRPC call failed: code={rpc_error.code()} details={rpc_error.details()!r}")
        raise

    status_name: str = sip.SipStatus.StatusType.Name(status.status_type)
    log.info(f"SIP status: {status_name} (account={status.account_name!r}) — {status.description}")
    log.info("DONE: register_account_example: run_sip_flow")
    return status


def main() -> None:
    """Parse CLI args, build the client, and run the representative SIP flow."""
    parser = argparse.ArgumentParser(description="Sip client handling example.")
    parser.add_argument(
        "--secure",
        default=USE_SECURE_CHANNEL,
        action="store_true",
        help="Open a TLS gRPC channel (default from ONDEWO_USE_SECURE_CHANNEL).",
    )
    args = parser.parse_args()

    log.info(f"START: register_account_example: main. host={HOST!r} port={PORT!r} secure={args.secure}")
    config: ClientConfig = build_config()
    client: Client = build_client(config=config, use_secure_channel=args.secure)
    run_sip_flow(client=client)
    log.info("DONE: register_account_example: main")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("register_account_example failed")
        sys.exit(1)
