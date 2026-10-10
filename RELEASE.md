# Release History

*****************

## Release ONDEWO SIP Python Client 5.5.0

### New Features

* [[OND233-367]](https://ondewo.atlassian.net/browse/OND233-367) Built against ondewo-sip-api 5.5.0: answering machine detection (`SipReportAnsweringMachineDetected`, `AnsweringMachineDetectionResult`, status `OUTGOING_CALL_ANSWERING_MACHINE_DETECTED`) and call control (`SipSetCallMediaControl`, the bidirectional `SipStreamCallAudio`, `SipStatus.call_id` / `bot_muted` / `listening_paused` / `call_audio_streams` / `sip_response_code`, `SipTransferCallRequest.outcome_timeout_ms`, `SipSetCallMediaControlRequest.participants_present`, `END_CALL_REASON_TRANSFERRED`).
* [[OND233-367]](https://ondewo.atlassian.net/browse/OND233-367) `Sip.set_call_media_control` and `Sip.stream_call_audio` on the sync and the async service. The async `stream_call_audio` is a plain method returning the grpc.aio async iterator (`async for response in sip.stream_call_audio(requests)`), never a coroutine.
* Call-scoped RPCs expect the `x-ondewo-expected-call-id` and `x-ondewo-sip-call-control-token` gRPC metadata; pass them on the stub (`client.services.sip.stub.<Rpc>(request, metadata=...)`) when the wrapper's client-wide metadata is not enough.

### Improvements

* `ondewo/sip/client/services/async_sip.py` is hand-written now (marker `ondewo:hand-written-async-service`), and `make create_async_services` leaves a marked file alone, as in ondewo-vtsi-client-python.
* The unit coverage gate covers `report_answering_machine_detected` again; it had dropped to 98.67%.
* `SipGetSipStatus` and `SipGetSipStatusHistory` carry `idempotency_level = NO_SIDE_EFFECTS` (sip-api 5.5.0), so `ondewo-client-utils` retries them on transient errors.
* `ondewo/sip` is also vendored by ondewo-vtsi-client-python: install both from the same sip-api release (5.5.0).

*****************

## Release ONDEWO SIP Python Client 5.4.3

### Bug Fixes

* [[OND211-2443]](https://ondewo.atlassian.net/browse/OND211-2443) `ClientConfig` no longer prints the mutual-TLS private key `grpc_client_key` (added by `ondewo-client-utils` 4.1.0). `BaseClientConfig` declares it `repr=False`, but this class overrides `__repr__` and ignored that flag, so `repr()` / `str()` rendered the PEM in clear text. It is now redacted as `***REDACTED***`, as is every other field declared `repr=False`.
* [[OND211-2443]](https://ondewo.atlassian.net/browse/OND211-2443) Dependency: `ondewo-client-utils>=4.1.1` on Python >= 3.12 (`>=3.2.0` below).
* [[OND211-2443]](https://ondewo.atlassian.net/browse/OND211-2443) `Client._initialize_services` and `AsyncClient._initialize_services` take a `BaseClientConfig` and raise `ValueError` for a config that is not a sip `ClientConfig`, instead of silencing the type check.
* Regenerated with [ondewo-proto-compiler 5.15.2](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.15.2).

*****************

## Release ONDEWO SIP Python Client 5.4.2

### Bug Fixes

* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Regenerated with [ondewo-proto-compiler 5.13.0](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.13.0).
* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Tooling: `conventional-pre-commit` now runs before `giticket` at the commit-msg stage - with giticket first, its `[OND221-2830] fix: ...` rewrite was no longer valid Conventional Commits and every commit on a ticket branch failed. `README.md` is prettier-ignored where `.prettierrc` sets `useTabs` and markdownlint's MD010 de-tabs the same blocks, and the codegen `docker run` invocations no longer pass `-it`, which fails outside a TTY.
* `ClientConfig` no longer prints its credentials. `@dataclass` generates a `__repr__` that renders every field, so `log.debug(f"...{config}")` — or any traceback carrying locals — wrote the Keycloak password and the gRPC certificate to the logs in clear text. `repr()` and `str()` now render `password` and `grpc_cert` as `***REDACTED***`. An unset or empty value still renders as `None` / `''`: the marker reads as "set and sensitive", which misleads when the real fault is that nobody set it.
* **Behaviour change** for anyone who parsed the repr: read the attribute (`config.password`, `config.grpc_cert`) instead. Only the rendered text changed — the fields themselves, equality and `dataclasses.asdict()` are untouched.

*****************

## Release ONDEWO SIP Python Client 5.4.1

### Bug Fixes

* Keycloak token providers are now shared per credential set instead of per ClientConfig object identity. The registry was keyed by id(config), and because a client keeps only the grpc channel its ClientConfig was collected as soon as the client was built; CPython then reused that address, so a later client could be handed the previous user's provider and silently authenticate as the wrong user.

### Improvements

* Tracking API Version [5.4.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.4.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 5.4.0

### Improvements

* Tracking API Version [5.4.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.4.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 5.3.0

### Improvements

* Tracking API Version [5.3.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.3.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 5.2.0

### Improvements

* Tracking API Version [5.2.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.2.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 5.1.1

### Improvements

* Added functionality to pass grpc options to grpc clients based on [ONDEWO CLIENT UTILS PYTHON 2.0.0](https://github.com/ondewo/ondewo-client-utils-python/releases/tag/2.0.0)

*****************

## Release ONDEWO SIP Python Client 5.1.0

### Improvements

* Tracking API Version [5.1.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.1.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 5.0.0

### Improvements

* Tracking API Version [5.0.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/5.0.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 4.0.1

### Bug Fixes

* Corrected return types of convenience methods of sip client endpoint calls

*****************

## Release ONDEWO SIP Python Client 4.0.0

### Improvements

* Tracking API
  Version [4.0.0](https://github.com/ondewo/ondewo-sip-api/releases/tag/4.0.0) ( [Documentation](https://ondewo.github.io/ondewo-sip-api/) )

*****************

## Release ONDEWO SIP Python Client 3.7.0

### New Features

* Updated ONDEWO-SIP API to [3.3.0](https://github.com/ondewo/ondewo-sip-api/releases/3.3.0)

*****************

## Release ONDEWO SIP Python Client 3.6.1

### Bug fix

* Generation of files and submodules

*****************

## Release ONDEWO SIP Python Client 3.6.0

### New Features

* Updated ONDEWO-SIP API to [3.2.0](https://github.com/ondewo/ondewo-sip-api/releases/3.2.0)

*****************

## Release ONDEWO SIP Python Client 3.5.0

### New Features

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) Added pre-commit hooks and adjusted files to them
* [[OND236-20]](https://ondewo.atlassian.net/browse/OND211-2039) Updated ONDEWO-SIP API
  to [3.1.0](https://github.com/ondewo/ondewo-sip-api/releases/3.1.0)

*****************

## Release ONDEWO SIP Python Client 3.4.0

### New Features

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Automated release process
* Updated ONDEWO-SIP API to [3.0.0](https://github.com/ondewo/ondewo-sip-api/releases/3.0.0)

*****************

## Release ONDEWO SIP Python Client 3.3.0

### New Features

* Uppdate grpc libraries.
* Refactor package generation.

*****************

## Release ONDEWO SIP Python Client 3.2.0

### New Features

* Supports muting and unmuting

*****************

## Release ONDEWO SIP Python Client 3.1.0

### New Features

* Regenerated the client from the updated ONDEWO-SIP API protos
* Upgraded grpcio to 1.42.0, protobuf to 3.19.1 and mypy-protobuf to 3.0.0
* Supports headers in get status when incoming call is connected

*****************

## Release ONDEWO SIP Python Client 2.3.0

### New Features

* Supports adding extra headers in calls and transfers when needed

*****************

## Release ONDEWO SIP Python Client 2.2.1

### New Features

* transfer requests included

*****************

## Release ONDEWO SIP Python Client 2.2.0

### New Features

* new endpoitns integrated, services have better defaults

*****************

## Release ONDEWO SIP Python Client 2.1.0

### New Features

* improved example script
* more endpoints
* in pypi

*****************

## Release ONDEWO SIP Python Client 2.0.0

### New Features

* grpc
