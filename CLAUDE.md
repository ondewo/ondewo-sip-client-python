# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working Principles

Behavioral guidelines to reduce common mistakes. They bias toward caution over speed; for trivial tasks, use judgment.

### Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Surgical changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that _your_ changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

### Goal-driven execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and
clarifying questions come before implementation rather than after mistakes.

## Logging

```python
from loguru import logger as log
```

- **Levels:** `log.trace()`, `log.debug()`, `log.info()`, `log.warning()`, `log.error()`, `log.exception()`. Choose by
  hotness/verbosity — `trace` for per-token / hot-path detail, `debug` for routine method entry/exit, `info` for notable
  lifecycle events, `warning` / `error` / `exception` for problems.
- **Interpolate with f-strings, not loguru's `{}` positional args.** Consistent with the Code Style rule, use
  `f"…{value}"`; only add the `f` prefix when the string actually interpolates (`"START: …"` with no params stays a
  plain string).
- **`START:` / `DONE:` bracketing.** Wrap a method (or other notable operation) with a `START:` line at entry and a
  `DONE:` line at exit, both naming `ClassName: method_name` (append `: param={value}` context where useful):

  ```python
  log.debug("START: IntentBertClassifier: predict")
  ...
  log.debug(f"DONE: IntentBertClassifier: predict. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

- **Timing uses `perf_counter()`, rendered `:.5f`.** Measure elapsed time with `time.perf_counter()` captured as a start
  value and subtracted at the `DONE:` line; always format the elapsed value with the `:.5f` spec:

  ```python
  from time import perf_counter

  start_time: float = perf_counter()
  ...
  log.info(f"DONE: SESSION SERVICER: DetectIntent. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

  Never measure a duration with `time.time()` — reserve `time.time()` for wall-clock timestamps (epoch seconds persisted
  to a DB / proto, unique-id or filename stamps). `perf_counter()` has an undefined epoch and must not be stored or
  compared across processes.

## Docstrings

Google-style, triple double-quotes:

```python
"""
Short imperative summary line.

Args:
    param_name (type):
        Description of the parameter.

Returns:
    type:
        Description of the return value.

Raises:
    ExceptionType:
        When this exception is raised.
"""
```

## GitHub Actions — the `tests` workflow is a REQUIRED gate

`.github/workflows/tests.yml` runs on **every push to every branch** (`branches: ["**"]`) and on every pull request.
It is a required gate, not advisory: a red run is a broken commit, not a note for later.

The job has exactly three commands (plus checkout and `setup-python` at **3.12**). Reproduce it locally with the
workflow's own commands — copied, not approximated:

```bash
python3.12 -m venv /tmp/sip-ci && . /tmp/sip-ci/bin/activate
python -m pip install --upgrade pip
pip install -e .
pip install pytest pytest-cov pytest-asyncio python-dotenv loguru
pytest tests/unit -q \
  --cov=ondewo.sip.utils.keycloak \
  --cov=ondewo.sip.client.client_config \
  --cov=ondewo.sip.client.services_interface \
  --cov=ondewo.sip.client.async_services_interface \
  --cov=ondewo.sip.client.services.sip \
  --cov=ondewo.sip.client.services.async_sip \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=100
```

To read the real verdict for a commit instead of guessing (no `gh` CLI needed):

```bash
curl -s "https://api.github.com/repos/ondewo/ondewo-sip-client-python/actions/runs?head_sha=$(git rev-parse HEAD)"
```

Things that are true of **this** repository and will mislead you otherwise — each one measured by running it:

- **There is no `uv` here.** No `pyproject.toml`, no `uv.lock`; packaging is `setup.py` + `requirements.txt`. There is
  no frozen lock to pin, so do not "modernize" the reproduction above into `uv run --frozen …` — there is nothing for
  it to resolve against, and the pinning argument that motivates `--frozen` elsewhere does not apply.
- **`requirements-dev.txt` is NOT the CI dependency set.** It lists neither `pytest-cov` nor `pytest-asyncio`, so an
  environment built from it rejects `--cov` as an unrecognised argument and fails all 22 async parametrisations. Install
  the workflow's explicit `pip install pytest pytest-cov pytest-asyncio python-dotenv loguru` line verbatim.
- **The `--cov=` targets are dotted MODULE names, and that form FAILS OPEN.** A module named in `--cov=` that the suite
  never imports is dropped from the report entirely: coverage emits only
  `CoverageWarning: Module … was never imported (module-not-imported)`, `TOTAL` stays `100.00%`, and the gate passes.
  The same file measured through a path-form source (`--cov=ondewo/sip/utils`) reports `0%` and fails. So a new
  hand-written module is invisible to this gate **twice**: once by not being in the list, and again even after somebody
  remembers to add it. **The line that buys coverage is a test that IMPORTS the module** — adding the `--cov=` flag
  alone buys nothing.
- **The six-module list is deliberate scoping, not an oversight — do not widen it into a directory scan.**
  `client.py` (88%), `async_client.py` (0%) and `async_services_container.py` (0%) are hand-written and sit outside the
  gate on purpose; `--cov=ondewo/sip/client` measures 91% and turns the build red. Widening the gate is legitimate, but
  it means writing the missing tests **first**, in the same change.
- **The workflow runs no linter and no type check.** `flake8` and `mypy` live only in the `Makefile` and
  `.pre-commit-config.yaml`, and the `Makefile` has no pytest target at all — so `make` cannot reproduce this gate and a
  green Actions run says nothing about lint or types. Run those separately before committing.
- `.coverage` and `coverage.xml` are written into the working tree by the run and are already in `.gitignore`.

## Git Commits

- **Never include Claude as author or co-author** in commit messages, PR descriptions, or any other text. Do not add
  `Co-Authored-By: Claude…` trailers, "Generated with Claude Code" footers, or any similar attribution.
- The user's own git author identity (already configured in git) is the only identity that should appear on commits.
- This rule overrides the default Claude Code commit-template guidance.
- **Never prepend the JIRA ticket ID** (e.g. `[OND211-2386]`) to the commit subject yourself. The `giticket` pre-commit
  hook reads the ticket from the branch name (`(feature|bugfix|support|hotfix)/<TICKET>-…`) and prepends `[<ticket>]`
  (with a trailing space) automatically. Writing the prefix manually produces a duplicate like
  `[OND211-2386] [OND211-2386] feat: …`. Write the subject as plain Conventional Commits (`feat: …`, `fix(scope): …`,
  `docs(types): …`) and let the hook add the prefix on commit.

## General Principles

- Follow existing patterns before introducing new abstractions.
- Keep changes minimal and consistent with surrounding code.
- Validate inputs early with descriptive, context-rich error messages.
- Use context managers for files, sockets, and thread pools.
- Prefer region comments for grouping methods in files that already use them.
- End edited Markdown and YAML files with a trailing newline.

## Release gotchas (hard-won this session)

These bit us during the 6.14.0 release. Keep them in mind when releasing.

- **Trust the registry, not the log.** `make release_all_clients` wraps each client in `|| echo "Already released …"`, so a _failed_ release is reported as "done". After any release, verify the GitHub release **and** the published package (PyPI / npm) directly.
- **`npm install failed after 5 attempts` in a release log is usually a red herring** — that text is the echo _inside_ the docker `RUN for i in 1..5; do npm install …` retry loop, not a real failure (`npm install` succeeds → `#10 DONE`). Look further down for the real error (a TTY error, an eslint failure, a `setup.py` error).
- **Codegen must run TTY-free.** The `docker run` that invokes the proto-compiler must not pass `-it` — non-interactively it fails with `cannot attach stdin to a TTY-enabled container because stdin is not a terminal`. Fix the script (drop `-it`), or run the whole release under a pseudo-TTY: `script -qc 'make …' /dev/null`.
- **Release Makefiles print secrets.** Some `docker run … -e <TOKEN>=…` recipe lines lack a leading `@`, so `make` echoes the expanded token. Rotate any token printed during a release; fix by prefixing the recipe line with `@`.
- The release auto-pulls the **latest** `ondewo-proto-compiler` tag.
- **npm package names are inconsistent** — e.g. the JS client publishes as `@ondewo/ondewo-nlu-client-js` (double `ondewo`), not `@ondewo/nlu-client-js`. Check `src/package.json`'s `name` before querying npm.
- **PyPI build needs setuptools.** The release image (`Dockerfile.utils`) is `python:3.12-slim`, which bundles no `setuptools`, so `python setup.py sdist bdist_wheel` dies with `ModuleNotFoundError: No module named 'setuptools'`. `Dockerfile.utils` must `pip install … setuptools wheel`.

## Python tooling — uv + ruff + mypy + pyproject.toml (this session's refactor)

This repo was migrated off `setup.py` / `.flake8` / `mypy.ini` to a single **pyproject.toml** with **uv**, **ruff**, and **mypy**. Going forward:

- **Build backend stays setuptools** (for PyPI compatibility). Build with `python -m build --no-isolation` or `uv build` — NOT `python setup.py sdist bdist_wheel` (setup.py is deleted). `Dockerfile.utils` installs `twine setuptools wheel build`.
- **Dependencies via uv + a committed `uv.lock`.** CI runs `uv sync --extra dev --frozen`. To add/change a dep: edit `[project.dependencies]`/`[project.optional-dependencies].dev` in pyproject.toml then `uv lock`.
- **Lint is ruff** (`[tool.ruff]`, line-length 120, generated `*_pb2*` excluded) — `uv run ruff check .`. flake8 is gone.
- **mypy config lives in `[tool.mypy]`.** Do **NOT** re-create `mypy.ini` — it silently _shadows_ the pyproject config. Generated `*_pb2*` modules get `ignore_errors` overrides.
- **Do NOT re-add `setup.py`** — with setuptools>=61 it conflicts with `[project]` on duplicated metadata.
- **PEP 625**: the sdist is now underscore-normalised (`ondewo_<name>-<v>.tar.gz`); anything that greps the tarball name by hand must use underscores.
- The version-bump release target edits the version in **pyproject.toml** (not setup.py); the release stages `pyproject.toml uv.lock`.

## uv migration — completed conversion (this session)

The repo is now fully on **uv** (not just pyproject.toml):

- `make setup_developer_environment_locally` bootstraps uv (installs it if missing), runs `uv sync --extra dev` (creates `.venv` + installs all runtime+dev deps + pre-commit), then `uv run pre-commit install`. **No conda** — the old `create_conda_env`/`setup_conda_env` scaffolding was removed.
- Every Makefile target uses uv: `uv sync --extra dev` (deps), `uv run pytest`/`ruff`/`mypy` (tools), `uv build` (wheel). No `pip install`, no `python -m build`, no `python setup.py`.
- New targets: `make ruff` / `make ruff_fix` / `make ruff_format` / `make mypy`. The `flake8` target is **removed**.
- Removed for good: `requirements.txt`, `requirements-dev.txt`, `setup.cfg` — deps + tool config live in `pyproject.toml`. Do **not** re-add them.
- `Dockerfile.utils` installs uv (`COPY --from=ghcr.io/astral-sh/uv`) and builds with uv; it no longer `COPY`s `requirements.txt`.
- **`[tool.mypy] python_version` must be `3.12`** wherever numpy 2.x is on the mypy path — its PEP-695 `type X = …` stubs fail to parse on < 3.12.
- The release `git commit` uses **`--no-verify`** so pre-commit hooks never gate an automated release.
- **Validated by a real PyPI publish** — `ondewo-t2s-client 6.5.0` was built with `uv build` and uploaded via twine end-to-end; the uv release pipeline works.

## `ondewo/sip` is also vendored by `ondewo-vtsi-client` — regenerate with care

This package ships `ondewo/sip` and nothing else (17 tracked files). But `ondewo-vtsi-client-python`
**vendors its own copy** of `ondewo/sip/*` (4 files), so in any venv that installs both — ondewo-vtsi
does — the two dists claim the same paths and **only one physical copy survives on disk**. Last
writer wins at install time.

There is no exception, no warning and no import error when the copies disagree: the loser's schema
simply is not there, and the symptom is a field that silently reads as unset. Verified against the
installed `.dist-info/RECORD` files: `ondewo_sip_client-5.3.0` and `ondewo_vtsi_client-8.2.0` both
claim `ondewo/sip/sip_pb2.py`, and at those versions the bytes are identical.

**So:** when you regenerate against a new `ondewo-sip-api`, tell whoever maintains
`ondewo-vtsi-client-python` to regenerate too, on the same api rev. ondewo-vtsi pins
`ondewo-sip-client>=5.3.0` (floating, unlike its exact `ondewo-s2t-client==7.3.1` /
`ondewo-t2s-client==6.2.0` pins), so a release of this client can start shadowing the vtsi-client
copy without anyone changing a pin. See ondewo-vtsi `CLAUDE.md` §3 for the full rule.

## `ClientConfig` must not print its secrets

`@dataclass` generates a `__repr__` that prints **every** field, so `log.debug(f"…{config}")` — or any
traceback carrying locals — wrote the ROPC `password` and the PEM `grpc_cert` to the log in clear text.
Downstream consumers really do log config objects: a repository-wide sweep in ondewo-vtsi found this class
among the leakers, alongside thirteen of its own dataclasses. All five ONDEWO Python clients had the same
defect and all five now carry the same fix.

`ondewo/sip/client/client_config.py` names the secrets once and renders around them:

```python
SECRET_FIELD_NAMES: ClassVar[FrozenSet[str]] = frozenset({"password", "grpc_cert"})
```

Four properties are load-bearing:

- **An empty secret renders as `''`, never as `***REDACTED***`.** The marker reads as "this is set and
  sensitive", which is actively misleading when the real fault is that nobody set it — usually the very
  thing being debugged. The `__repr__` therefore redacts only a _truthy_ value.
- **A new secret field must join `SECRET_FIELD_NAMES` in the same commit.** That frozenset is the entire
  policy; nothing infers sensitivity from a field name.
- **Redaction covers `repr()` / `str()` only.** Measured on the real class: `to_json()`, `to_dict()` and
  `dataclasses.asdict()` still return the plaintext password, and `to_json()` renders the certificate as a
  byte array. That is deliberate, because `@dataclass_json` has to round-trip through `from_json` — so
  never log a serialized config, and do not "fix" it by redacting there.
- **The guard is behavioural.** `tests/unit/utils/test_client_config_redacts_secrets.py` builds a
  `ClientConfig` with distinctive planted values and reads its `repr`. It does not grep for `__repr__`,
  because a grep passes just as well for a `__repr__` that prints the secret anyway. It also asserts each
  secret is really **on the object** (`config.password == PASSWORD`) before asserting it is absent from the
  repr — reading only the repr would pass vacuously against unfixed code. The certificate is compared
  against `GRPC_CERT.encode()`, since `BaseClientConfig.__post_init__` encodes it to `bytes`; comparing to
  the `str` would fail while the redaction it guards worked perfectly.

Run it with `uv run pytest tests/unit/utils/test_client_config_redacts_secrets.py -q` — 5 tests.

**The fix is unreleased, and the version string cannot tell you that.** `git tag --contains HEAD` is empty
here; the redaction commit sits _after_ `PREPARING FOR RELEASE 5.4.1` and did not bump the version, so this
tree still says `5.4.1` while the published `5.4.1` has the leak. ondewo-vtsi pins
`ondewo-sip-client==5.4.1`, so it keeps resolving to the artifact without the fix until a new version is
cut. A release, not a rebuild, is what closes this.

## The two commit-msg hooks must run in this order

`.pre-commit-config.yaml` lists `conventional-pre-commit` **before** `giticket`, and the order is the whole
point. pre-commit runs hooks in file order, and `giticket` rewrites the subject to
`[OND211-2418] <subject>`, which is not a valid Conventional Commit. With `giticket` first the validator is
handed the prefix the other hook just added and rejects it, so **no conforming commit message exists at
all** — one hook failing on the other hook's output. The only escapes were `--no-verify` (which also skips
ruff, ruff-format, mypy and uv-lock) or renaming the branch away from its ticket, and this repo's history
shows the result: subjects that are not Conventional Commits at all.

This repo had the wrong order until the redaction commit fixed it. So: type the plain subject
(`fix(client-config): …`), let the validator see exactly that, and let `giticket` decorate it afterwards.
Never write the `[TICKET]` prefix yourself — that yields `[OND211-2418] [OND211-2418] …`.

One cosmetic leftover: an orphaned `# Enforce Conventional Commits on the commit message.` comment sits at
the end of the file, where the hook used to be. It documents nothing now.

## Releasing: preflight and the traps that have actually bitten

Written after a release program across every ONDEWO client in one session. Each item below
cost real time or a broken artefact; every statement is derived from THIS repo's Makefile.

### Before you touch the version, check the released tag is in `master`

Releases here are cut from a `release/<version>` branch and are **not always merged back**, so
`master` can be missing work that is already published — and because a later version number
sorts above the unmerged one, a consumer upgrading silently loses it. The ondewo-nlu-client-python
7.1.0 release was exactly this: it shipped from a `master` that had never seen 7.0.5's
offline-token hand-off, so PyPI's newest release was a regression against its predecessor.

```bash
latest=$(git tag --sort=-v:refname | head -1)
git merge-base --is-ancestor "$latest" master && echo "in master" || echo "NOT in master -- merge first"
```

A fast-forward (`git merge --ff-only <tag>`) is the common case. A true merge needs care: resolve
metadata toward `master` and keep BOTH release-note sections, newest first — a reader upgrading
from the older line still needs the older entry.

### `git add` on a dirty submodule stages the WRONG commit

This repo has submodules (`ondewo-proto-compiler`, `ondewo-sip-api`). If a submodule's working
tree is dirty, `git add <submodule>` stages **its current HEAD**, not the pointer you resolved
during a merge — silently regressing it to an older commit. `git checkout master -- <submodule>`
fixes the index but the next `git add` re-breaks it. Move the working tree instead:

```bash
want=$(git ls-tree master <submodule> | awk '{print $3}')
git -C <submodule> checkout -q "$want" && git add <submodule>
```

### The release notes are sliced by an EXACTLY-CASED heading

`CURRENT_RELEASE_NOTES` slices `RELEASE.md` with a perl range. In THIS repo the opening
pattern is, verbatim:

```text
Release ONDEWO SIP Python Client ${ONDEWO_SIP_VERSION}
```

So the heading of a new entry must read exactly `## Release ONDEWO SIP Python Client <version>`. **This wording is
not consistent across the ONDEWO repos** — some say `... <Name> Client`, some `... Client
<Name>` with the words reversed, the API repos say `... API` with no `Client` at all, and the
casing varies (`Js`, `Nodejs`, `Typescript`, `Survey`). Do not carry a heading over from a
sibling repo. Copy the PREVIOUS entry in this file and change only the version, or read the
pattern above out of the Makefile.

A heading that does not match yields an **empty slice**, and the GitHub release is then
created with empty notes or fails outright. Verify before releasing:

```bash
grep -c '^## Release ONDEWO SIP Python Client ' RELEASE.md     # must be >= 1 for your new version
```

### Publish order decides how a partial failure is recovered

`make release` in this repo runs:

1. `create_release_branch`
2. `create_release_tag`
3. `release_to_github_via_docker`
4. `push_to_pypi_via_docker`
5. `push_to_pypi`

The **PyPI publish happens LAST**. So a failure before it means nothing shipped, but the
branch, tag and GitHub release may already exist — and `spc` will then refuse a re-run. Recover
by running only the remaining step, not the whole target.

### Verify against the registry, with the REAL package name

This package publishes as **`ondewo-sip-client`**, which is not always the repository name — the JS client
publishes as `@ondewo/ondewo-nlu-client-js` (doubled `ondewo`), so a lookup by repo name returns
a 404 that reads like a failed release. Check the name in the manifest first, then:

```bash
curl -s https://pypi.org/pypi/ondewo-sip-client/json | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])"
```

### The `mypy` pre-commit hook is `language: system`

It runs whatever `mypy` is on `PATH`, so a `git commit` outside the project venv fails with
`Executable mypy not found` even though `uv run mypy` passes. Commit with the venv on `PATH`
rather than reaching for `--no-verify`:

```bash
PATH="$PWD/.venv/bin:$PATH" git commit -m "..."
```

### The release prints credentials — read the log BEFORE you scrub it

`make ondewo_release` clones `ondewo-devops-accounts` and passes the registry and GitHub tokens on
the make command line, so they are echoed into the console and into any transcript capturing it.
This is a known and accepted property of the shared release path: do **not** re-plumb the recipe.
Redirect the run to a file, read it through a filter, and shred the file afterwards — and read it
**before** shredding, or a genuine failure is lost with the secrets:

```bash
umask 077; make ondewo_release > /tmp/rel.log 2>&1; echo "RC=$?"
grep -avE 'TOKEN|PASSWORD|USERNAME|_authToken' /tmp/rel.log | tail -20   # read FIRST
shred -u /tmp/rel.log; rm -rf ondewo-devops-accounts                     # then scrub
```
