<div align="center">
  <table>
    <tr>
      <td>
        <a href="https://ondewo.com/en/products/natural-language-understanding/">
            <img width="400px" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/ondewo_we_automate_your_phone_calls.png"/>
        </a>
      </td>
    </tr>
    <tr>
        <td align="center">
          <a href="https://www.linkedin.com/company/ondewo "><img width="40px" src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png"></a>
          <a href="https://www.facebook.com/ondewo"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/733/733547.png"></a>
          <a href="https://twitter.com/ondewo"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/733/733579.png"> </a>
          <a href="https://www.instagram.com/ondewo.ai/"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/174/174855.png"></a>
        </td>
    </tr>
  </table>
  <h1>
  Ondewo SIP Client Python Library
  </h1>
</div>

This library facilitates the interaction between a user and a CAI server. It achieves this by providing a higher-level interface mediator.

This higher-level interface mediator is structured around a series of python files generated from protobuf files. These protobuf files specify the details of the interface, and can be used to generate code in 10+ high-level languages. They are found in the [ONDEWO SIP API](https://github.com/ondewo/ondewo-sip-api) along with the older Google protobufs from Dialogueflow that were used at the start. The [ONDEWO PROTO-COMPILER](https://github.com/ondewo/ondewo-proto-compiler) will generate the needed files directly in this library.

## Python Installation

You can install the library by installing it directly from the PyPi:

```bash
pip install ondewo-sip-client
```

Or, you could clone it and install the requirements:

```bash
git clone git@github.com:ondewo/ondewo-sip-client-python.git
cd ondewo-sip-client-python
make setup_developer_environment_locally
```

## Repository Structure

```
.
├── examples
│   ├── __init__.py
│   └── register_account_example.py
├── ondewo
│   ├── sip
│   │   ├── client
│   │   │   ├── services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── async_sip.py
│   │   │   │   └── sip.py
│   │   │   ├── __init__.py
│   │   │   ├── async_client.py
│   │   │   ├── async_services_container.py
│   │   │   ├── async_services_interface.py
│   │   │   ├── client.py
│   │   │   ├── client_config.py
│   │   │   ├── services_container.py
│   │   │   └── services_interface.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── keycloak.py           <----- D18 Keycloak headless offline-token provider
│   │   ├── __init__.py
│   │   ├── sip_pb2_grpc.py
│   │   ├── sip_pb2.py
│   │   └── sip_pb2.pyi
│   └── __init__.py
├── ondewo-proto-compiler
├── ondewo-sip-api
├── tests
├── CONTRIBUTING.md
├── Dockerfile.utils
├── LICENSE
├── Makefile
├── MANIFEST.in
├── pyproject.toml
├── README.md
├── RELEASE.md
├── sip_config.json
└── uv.lock
```

## Build

The `make build` command is dependent on 2 `repositories` and their speciefied `version`:

- [ondewo-sip-api](https://github.com/ondewo/ondewo-sip-api) -- `ONDEWO_SIP_API_GIT_BRANCH` in `Makefile`
- [ondewo-proto-compiler](https://github.com/ondewo/ondewo-proto-compiler) -- `ONDEWO_PROTO_COMPILER_GIT_BRANCH` in `Makefile`

It will generate a `_pb2.py`, `_pb2.pyi` and `_pb2_grpc.py` file for every `.proto` in the api submodule.

> :warning: All Files in the `ondewo` folder that dont have `pb2` in their name are handwritten, and therefor need to be manually adjusted to any changes in the proto-code.

## Examples

The `/examples` folder provides a possible implementation of this library. To run an example, simple execute it like any other python file. To specify the server and credentials, you need to provide an environment file with the following variables:

- host `// The hostname of the Server - e.g. 127.0.0.1`
- port `// Port of the Server - e.g. 6600`
- user_name `// Username - same as you would use in AIM`
- password `// Password of the user`
- grpc_cert `// gRPC Certificate of the server`

## Authentication

The client authenticates via the Keycloak headless offline-token flow (D18). Set the Keycloak fields on the `ClientConfig` alongside `user_name`/`password`:

- keycloak_url `// Base URL of the Keycloak server - e.g. https://my-host/auth`
- realm `// Keycloak realm - e.g. ondewo-ccai-platform`
- client_id `// Public SDK client id - e.g. ondewo-sip-cai-sdk-public (no client secret)`

On first use the SDK performs a one-time ROPC `offline_access` login and then auto-refreshes the short-lived access token in the background. Every RPC carries the resulting `Authorization: Bearer <jwt>` header, injected via the service wrapper's `self.metadata`.

Leaving the three Keycloak fields empty attaches no auth token (for use against a plaintext server or an Envoy ingress that injects auth).

## Automatic Release Process

The entire process is automated to make development easier. The actual steps are simple:

TODO after Pull Request was merged in:

- Checkout master:

  ```shell
  git checkout master
  ```

- Pull the new stuff:

  ```shell
  git pull
  ```

- (If not already, run the `setup_developer_environment_locally` command):

  ```shell
  make setup_developer_environment_locally
  ```

- Update the `ONDEWO_SIP_VERSION` in the `Makefile`
- Add the new Release Notes in `RELEASE.md` in the format:

  ```
  ## Release ONDEWO SIP Python Client X.X.X       <---- Beginning of Notes

     ...<NOTES>...

  *****************                      <---- End of Notes
  ```

- Release:

  ```shell
  make ondewo_release
  ```

---

`make ondewo_release` runs these steps, in this order, and stops at the first one that fails. The order is pinned by
`tests/unit/test_release_runs_in_a_fresh_clone.py` and is the same in every `ondewo-sip-client-<language>`
repository, so `ondewo-sip-api`'s release driver treats them alike.

1. `spc` (read-only, no credentials): the branch `release/<version>` and the tag `<version>` are not on origin
   (`git ls-remote --exit-code`, exact refs), PyPI does not serve `ondewo-sip-client <version>` yet, and `RELEASE.md`
   carries exactly one `## Release ONDEWO SIP Python Client <version>` heading (matched anchored, dots escaped) with
   a non-empty body.
2. Load `GITHUB_GH_TOKEN`, `PYPI_USERNAME` and `PYPI_PASSWORD` from `ondewo-devops-accounts`, then **delete that
   clone** before anything else runs, and also when the clone or the release fails. The clone lives in a `mktemp`
   directory, never in this repository. When `DEVOPS_ACCOUNT_DIR` points at an existing clone (the driver clones once
   for all clients), it is used and not cloned again.
3. `release_preflight` (read-only): the host tools exist, `spc` again, and both credentials are VALID:
   - GitHub: `gh api repos/ondewo/ondewo-sip-client-python --jq .permissions.push` prints `true`.
   - PyPI has no read-only identity call, so the probe re-uploads the newest file that is already on PyPI. PyPI checks
     the credential and the upload permission on this project first (`403` when either fails) and only then refuses
     the existing file (`400 File already exists`). A pass therefore proves the credential may upload to
     `ondewo-sip-client`, and it cannot publish anything new.
4. `build` (regenerates the code from `ondewo-sip-api`), the pre-commit hooks, `check_build` and `make test` (ruff,
   mypy and the unit suite with the coverage gate). These steps run with the credentials removed from their
   environment.
5. Commit locally (only when something changed), upload to PyPI, and wait until the PyPI JSON API serves the version.
   PyPI comes first because it is the one step that cannot be undone.
6. Push, create and push `release/<version>` and the tag `<version>`, create the GitHub release from the `RELEASE.md`
   section (an empty body is refused).
7. `release_verify` (read-only, also run by the driver afterwards): the tag is on origin, the GitHub release has a
   non-empty body, and PyPI serves the version (polled 20 x 30 s; `VERIFY_ATTEMPTS` / `VERIFY_INTERVAL_S` override).

`release_preflight` and `release_verify` also run standalone: with only an absolute `DEVOPS_ACCOUNT_DIR` set they read
the credentials from that clone, e.g. `make release_verify DEVOPS_ACCOUNT_DIR=/abs/path/ondewo-devops-accounts`.

Host requirements: `docker`, `git`, `make`, `perl`, `curl` and `uv`. `gh`, `twine` and the package build run in the
pinned `Dockerfile.utils` image (exact uv, twine and gh versions, base images by digest), and gh reads the token from
`GH_TOKEN` per call, so nothing is stored in `~/.config/gh`. No credential is ever put on a command line.
