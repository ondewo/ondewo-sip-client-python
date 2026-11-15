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
"""
The generated ``ondewo.sip.sip_pb2`` carries the ondewo-sip-api 5.7.0 surface: transfer delegation, the delegated
transfer record, ``SipStatus.capabilities`` and the warm-transfer outcome notice, with their wire field numbers.
"""

from typing import (
    Dict,
    List,
    Optional,
)

import pytest
from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
)

from ondewo.sip import sip_pb2


@pytest.mark.parametrize(
    "enum_name, values",
    [
        (
            "SipTransferDelegation",
            {
                "SIP_TRANSFER_DELEGATION_UNSPECIFIED": 0,
                "SIP_TRANSFER_DELEGATION_CLAIM": 1,
                "SIP_TRANSFER_DELEGATION_EXECUTE": 2,
                "SIP_TRANSFER_DELEGATION_DISCARD": 3,
            },
        ),
        (
            "SipWarmTransferOutcome",
            {
                "SIP_WARM_TRANSFER_OUTCOME_UNSPECIFIED": 0,
                "SIP_WARM_TRANSFER_OUTCOME_DECLINED": 1,
                "SIP_WARM_TRANSFER_OUTCOME_UNREACHABLE": 2,
                "SIP_WARM_TRANSFER_OUTCOME_DELEGATION_EXPIRED": 3,
            },
        ),
    ],
)
def test_top_level_enum_values(enum_name: str, values: Dict[str, int]) -> None:
    enum: EnumDescriptor = sip_pb2.DESCRIPTOR.enum_types_by_name[enum_name]
    assert {value.name: value.number for value in enum.values} == values


@pytest.mark.parametrize(
    "message_name, fields",
    [
        (
            "SipDelegatedTransfer",
            {"request_id": 1, "requested_at": 2, "target_is_phone_number": 3, "transfer_id": 4, "headers": 5},
        ),
        (
            "SipWarmTransferOutcomeNotice",
            {
                "request_id": 1,
                "outcome": 2,
                "intro_session": 3,
                "callee_display_name": 4,
                "cause": 5,
                "fallback_text": 6,
            },
        ),
    ],
)
def test_new_messages_and_their_field_numbers(message_name: str, fields: Dict[str, int]) -> None:
    message: Descriptor = sip_pb2.DESCRIPTOR.message_types_by_name[message_name]
    assert {field.name: field.number for field in message.fields} == fields


@pytest.mark.parametrize(
    "message_name, fields",
    [
        ("SipTransferCallRequest", {"delegation": 4, "delegated_request_id": 5}),
        (
            "SipStatus",
            {"delegated_transfer": 17, "capabilities": 18, "warm_transfer_outcome_notice_status": 19},
        ),
        ("SipSetCallMediaControlRequest", {"warm_transfer_outcome": 5}),
    ],
)
def test_new_fields_on_existing_messages(message_name: str, fields: Dict[str, int]) -> None:
    message: Descriptor = sip_pb2.DESCRIPTOR.message_types_by_name[message_name]
    assert {name: message.fields_by_name[name].number for name in fields} == fields


def test_status_capabilities_is_repeated_and_the_notice_status_enum_has_every_value() -> None:
    status: sip_pb2.SipStatus = sip_pb2.SipStatus(capabilities=["warm-transfer-outcome-notice"])
    assert list(status.capabilities) == ["warm-transfer-outcome-notice"]
    notice_status: Optional[EnumDescriptor] = sip_pb2.SipStatus.DESCRIPTOR.fields_by_name[
        "warm_transfer_outcome_notice_status"
    ].enum_type
    assert notice_status is not None
    names: List[str] = [value.name for value in notice_status.values]
    assert len(names) == 6
    assert [value.number for value in notice_status.values] == [0, 1, 2, 3, 4, 5]


def test_a_delegated_transfer_request_round_trips() -> None:
    request: sip_pb2.SipTransferCallRequest = sip_pb2.SipTransferCallRequest(
        transfer_id="+431234",
        delegation=sip_pb2.SIP_TRANSFER_DELEGATION_CLAIM,
        delegated_request_id="req-1",
    )
    parsed: sip_pb2.SipTransferCallRequest = sip_pb2.SipTransferCallRequest.FromString(request.SerializeToString())
    assert parsed.delegation == sip_pb2.SIP_TRANSFER_DELEGATION_CLAIM
    assert parsed.delegated_request_id == "req-1"
