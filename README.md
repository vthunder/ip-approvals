# ip-approvals

One JSON record per code batch submitted for prior approval, under
`records/<project>/<date>-<sha>.json`. The `ip-approval-gate` workflow in
each project repo reads this repo on every pull request to `main` and
refuses the merge unless a record matches the PR's diff hash and is either
past its objection window or explicitly approved. Records are written by
`sandmill-infra/bin/ip-submit.sh`.

Build configuration (own package versions, compiler/base-image/CI-action
pins, dependency updates for upstream security fixes, CI/deployment
configuration) needs no prior approval: see
[policy/build-config.md](policy/build-config.md). Those records carry
`"exempt": "build-config"`.

The Status table below is rewritten by `.github/workflows/status.yml`
(`scripts/status.py`) every 30 minutes and whenever a record changes.

## Status

<!-- status:start -->
| repo | stage | head | mirror checks | approval | main | deploys | advisory ignores |
|---|---|---|---|---|---|---|---|
| [browserid-ng](https://github.com/vthunder/browserid-ng) | ✅ merged | [`c66a1fb3`](https://github.com/vthunder/browserid-ng-staging/commit/c66a1fb3) |  | exempt build-config 2026-11-13 ([record](records/browserid-ng/2026-11-13-c66a1fb3.json)) | [`e9e7a45a`](https://github.com/vthunder/browserid-ng/commits/main) | [6 ok, last 2026-11-13](https://github.com/vthunder/browserid-ng/actions) | next review 2026-12-15 |
| [mingo](https://github.com/vthunder/mingo) | ✅ merged | [`65b39a1d`](https://github.com/vthunder/mingo-staging/commit/65b39a1d) |  | approved 2026-11-12 ([record](records/mingo/2026-11-08-65b39a1d.json)) | [`097e6f3c`](https://github.com/vthunder/mingo/commits/main) | [2 ok, last 2026-11-12](https://github.com/vthunder/mingo/actions) | next review 2027-02-01 |
| [sbo](https://github.com/vthunder/sbo) | ✅ merged | [`d8a264aa`](https://github.com/vthunder/sbo-staging/commit/d8a264aa) |  | exempt build-config 2026-11-13 ([record](records/sbo/2026-11-13-d8a264aa.json)) | [`eb1b73ad`](https://github.com/vthunder/sbo/commits/main) | [via mingo (pinned SBO_REV)](https://github.com/vthunder/sbo/actions) | next review 2026-12-15 |
| [browserid-pay](https://github.com/vthunder/browserid-pay) | ✅ merged | [`af32cc4b`](https://github.com/vthunder/browserid-pay-staging/commit/af32cc4b) |  | approved 2026-11-12 ([record](records/browserid-pay/2026-11-08-af32cc4b.json)) | [`e4f99d98`](https://github.com/vthunder/browserid-pay/commits/main) | [4 ok, last 2026-11-12](https://github.com/vthunder/browserid-pay/actions) | next review 2027-02-01 |
| [browserid-bsky](https://github.com/vthunder/browserid-bsky) | ✅ merged | [`1a1d2f32`](https://github.com/vthunder/browserid-bsky-staging/commit/1a1d2f32) |  | approved 2026-11-12 ([record](records/browserid-bsky/2026-11-08-1a1d2f32.json)) | [`85285b61`](https://github.com/vthunder/browserid-bsky/commits/main) | [1 ok, last 2026-11-12](https://github.com/vthunder/browserid-bsky/actions) | next review 2027-02-01 |

To mention in the next submission email:

- browserid-ng: rusqlite 0.32 -> 0.41.1 for the bundled SQLite fix (CVE-2026-119375); the upgrade also needed one rusqlite feature flag (fallible_uint) to keep the previous behaviour, no source changes ([record](records/browserid-ng/2026-11-13-c66a1fb3.json))

Last change 2026-11-13 19:14 UTC; checked every 30 minutes by `.github/workflows/status.yml` (`scripts/status.py`).
<!-- status:end -->
