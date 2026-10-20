# OAuth Echo Python 3 regression repair

## Goal

Keep the public constructor/post API and repair two source-proved failures: the constructor references undefined `realm` instead of its `oauth_realm` argument; post calls `dict.iteritems()`. Add a minimal hosted gate for the existing offline suite and package build under the subsequent all-open-PR authorization.

## State

- Base: `e8974e26eb0f383c233a7aa037a98358d7ee8fe8`, authenticated current accessibleapps/oauth_echo_client master.
- Isolated worktree: task-6/worktrees/oauth_echo_client; branch modernize/task6-oauth_echo_client. Canonical checkout and same-name non-Git user directory are untouched.
- Source inspected: oauth_echo_client.py and setup.py in full; real TwishortAPI constructor/post caller in sibling twishort.py. No manifest or shared dependency pin change.
- No repository guidance, existing test files, hosted CI, hooks configuration, README, or documented full-check command exists in this base.
- Tests were authored first. `python -B -m unittest -v test_oauth_echo_client.py` failed with the exact constructor `NameError` and post `AttributeError` on CPython 3.13.6. They import the real module with an OAuth signing double and mocked requests session; no service, credentials, login, or upload is contacted.
- After the two substitutions, that same focused command passed both tests in 0.740 seconds. No dependency resolver or build was run; setup.py is unchanged and this base has no lock file.
- The ordinary staged whitespace check reports the two changed source lines because this file is stored with CRLF. Read-only byte inspection confirmed exactly 37 CRLF/37 LF in both base and working file. Preserve that existing format; use the per-command CR-at-EOL whitespace interpretation for this diff. No repository or global setting is changed. No pre-commit hook or configured hooks path exists; setup.py's working/base blob remains `9b25ad3dd5086dd10889a5c4cb895ba0ae500a1e`.

## Decisions and why

Use `oauth_realm` and `.items()`, which preserve the API and remain valid on Python 2 as well as Python 3. Do not change signing policy, transport behavior, endpoints, package versions, or dependency declarations.

## Surprises

The repository's last commit describes a Python 3 rewrite, but these two failures remain. The available runtime is CPython 3.13.6. Full documented checks are unavailable; only the actively authored regression file will be run locally.

## Next step

CI amendment is isolated on repair/task6-oauth_echo_client-ci from published #1 head 4831f15e4e7b126e400c31eabc4432b3d9f8d0e3. Both original local and published tips are preserved at backup/task6-oauth_echo_client-ci-local and backup/task6-oauth_echo_client-ci-published; original worktree files are untouched. Default master has no tests (only module and setup.py), so the coordinator authorized CI directly on the existing feature suite rather than a zero-test prerequisite. Actions enabled=true was verified read-only. One Linux/Python 3.12 job runs the full two-test suite, using only the already-declared requests dependency; OAuth is mocked and requests.session/post are mocked. It builds the existing setup.py package and requires both artifacts. No source/dependency changes or service calls. Latest official action releases were resolved to pinned commits; Actions Dependabot maintains them.

Local amendment validation on Python 3.12: full two-test suite passed (requests resolved to 2.34.2); uv build produced both exact package artifacts, with the pre-existing missing-README sdist warning. actionlint 1.7.12 passed; zizmor 1.31.1 offline reported no findings (one default suppression). Generated build/ and egg-info artifacts are untracked and not staged. Return the exact local head for coordinator review before any explicit-lease push to the original PR ref. Actual Claude review of the final augmented head and green hosted checks are required before merge. Mock tests do not prove live OAuth service compatibility.
