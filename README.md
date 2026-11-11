# ip-approvals

One JSON record per code batch submitted for prior approval, under
`records/<project>/<date>-<sha>.json`. The `ip-approval-gate` workflow in
each project repo reads this repo on every pull request to `main` and
refuses the merge unless a record matches the PR's diff hash and is either
past its objection window or explicitly approved. Records are written by
`sandmill-infra/bin/ip-submit.sh`.

The Status table below is rewritten by `.github/workflows/status.yml`
(`scripts/status.py`) every 30 minutes and whenever a record changes.

## Status

<!-- status:start -->
| repo | stage | head | mirror checks | approval | main | deploys |
|---|---|---|---|---|---|---|
| [browserid-ng](https://github.com/vthunder/browserid-ng) | ⏳ awaiting approval | [`ccf475a4`](https://github.com/vthunder/browserid-ng-staging/commit/ccf475a4) | 9/9 green | submitted 2026-11-08, deemed approved 2026-11-22 (11 d) ([record](records/browserid-ng/2026-11-08-ccf475a4.json)) | [`70e77906`](https://github.com/vthunder/browserid-ng/commits/main) | [6 ok, last 2026-11-06](https://github.com/vthunder/browserid-ng/actions) |
| [mingo](https://github.com/vthunder/mingo) | ⏳ awaiting approval | [`65b39a1d`](https://github.com/vthunder/mingo-staging/commit/65b39a1d) | 4/4 green | submitted 2026-11-08, deemed approved 2026-11-22 (11 d) ([record](records/mingo/2026-11-08-65b39a1d.json)) | [`e0e6d42b`](https://github.com/vthunder/mingo/commits/main) | [2 ok, last 2026-09-19](https://github.com/vthunder/mingo/actions) |
| [sbo](https://github.com/vthunder/sbo) | ⏳ awaiting approval | [`55243ddc`](https://github.com/vthunder/sbo-staging/commit/55243ddc) | 4/4 green | submitted 2026-11-08, deemed approved 2026-11-22 (11 d) ([record](records/sbo/2026-11-08-55243ddc.json)) | [`4033e1fa`](https://github.com/vthunder/sbo/commits/main) | [via mingo (pinned SBO_REV)](https://github.com/vthunder/sbo/actions) |
| [browserid-pay](https://github.com/vthunder/browserid-pay) | ⏳ awaiting approval | [`af32cc4b`](https://github.com/vthunder/browserid-pay-staging/commit/af32cc4b) | 8/8 green | submitted 2026-11-08, deemed approved 2026-11-22 (11 d) ([record](records/browserid-pay/2026-11-08-af32cc4b.json)) | [`e7e1a73b`](https://github.com/vthunder/browserid-pay/commits/main) | [4 ok, last 2026-09-20](https://github.com/vthunder/browserid-pay/actions) |
| [browserid-bsky](https://github.com/vthunder/browserid-bsky) | ⏳ awaiting approval | [`1a1d2f32`](https://github.com/vthunder/browserid-bsky-staging/commit/1a1d2f32) | 4/4 green | submitted 2026-11-08, deemed approved 2026-11-22 (11 d) ([record](records/browserid-bsky/2026-11-08-1a1d2f32.json)) | [`1f34ad8b`](https://github.com/vthunder/browserid-bsky/commits/main) | [1 ok, last 2026-11-04](https://github.com/vthunder/browserid-bsky/actions) |

Last change 2026-11-11 12:27 UTC; checked every 30 minutes by `.github/workflows/status.yml` (`scripts/status.py`).
<!-- status:end -->
