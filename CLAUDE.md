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
