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
| repo | stage | head | mirror checks | approval | main | deploys |
|---|---|---|---|---|---|---|
| [browserid-ng](https://github.com/vthunder/browserid-ng) | ✅ merged | [`ccf475a4`](https://github.com/vthunder/browserid-ng-staging/commit/ccf475a4) |  | approved 2026-11-12 ([record](records/browserid-ng/2026-11-08-ccf475a4.json)) | [`270c355c`](https://github.com/vthunder/browserid-ng/commits/main) | [6 ok, last 2026-11-12](https://github.com/vthunder/browserid-ng/actions) |
| [mingo](https://github.com/vthunder/mingo) | ✅ merged | [`65b39a1d`](https://github.com/vthunder/mingo-staging/commit/65b39a1d) |  | approved 2026-11-12 ([record](records/mingo/2026-11-08-65b39a1d.json)) | [`097e6f3c`](https://github.com/vthunder/mingo/commits/main) | [2 ok, last 2026-11-12](https://github.com/vthunder/mingo/actions) |
| [sbo](https://github.com/vthunder/sbo) | 🛠️ in progress | [`9881a478`](https://github.com/vthunder/sbo-staging/commit/9881a478) | 1 failing (rc / supply-chain) | not submitted ([record](records/sbo/2026-11-08-55243ddc.json)) | [`041eceaa`](https://github.com/vthunder/sbo/commits/main) | [via mingo (pinned SBO_REV)](https://github.com/vthunder/sbo/actions) |
| [browserid-pay](https://github.com/vthunder/browserid-pay) | ✅ merged | [`af32cc4b`](https://github.com/vthunder/browserid-pay-staging/commit/af32cc4b) |  | approved 2026-11-12 ([record](records/browserid-pay/2026-11-08-af32cc4b.json)) | [`e4f99d98`](https://github.com/vthunder/browserid-pay/commits/main) | [4 ok, last 2026-11-12](https://github.com/vthunder/browserid-pay/actions) |
| [browserid-bsky](https://github.com/vthunder/browserid-bsky) | ✅ merged | [`1a1d2f32`](https://github.com/vthunder/browserid-bsky-staging/commit/1a1d2f32) |  | approved 2026-11-12 ([record](records/browserid-bsky/2026-11-08-1a1d2f32.json)) | [`85285b61`](https://github.com/vthunder/browserid-bsky/commits/main) | [1 ok, last 2026-11-12](https://github.com/vthunder/browserid-bsky/actions) |

Last change 2026-11-12 23:14 UTC; checked every 30 minutes by `.github/workflows/status.yml` (`scripts/status.py`).
<!-- status:end -->
