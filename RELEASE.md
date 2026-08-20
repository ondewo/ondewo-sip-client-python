# Release History

*****************

## Release ONDEWO SIP Python Client 5.4.2

### Bug Fixes

* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Regenerated with [ondewo-proto-compiler 5.13.0](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.13.0).
* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Tooling: `conventional-pre-commit` now runs before `giticket` at the commit-msg stage - with giticket first, its `[OND221-2830] fix: ...` rewrite was no longer valid Conventional Commits and every commit on a ticket branch failed. `README.md` is prettier-ignored where `.prettierrc` sets `useTabs` and markdownlint's MD010 de-tabs the same blocks, and the codegen `docker run` invocations no longer pass `-it`, which fails outside a TTY.

*****************

## Unreleased

### Bug Fixes

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

## Release ONDEWO SIP Python Client 3.0.0

### New Features

* Supports adding extra headers in calls and transfers when needed
* Supports headers in get status when incoming call is connected

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
