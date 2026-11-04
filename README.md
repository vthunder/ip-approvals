# ip-approvals

One JSON record per code batch submitted for prior approval, under
`records/<project>/<date>-<sha>.json`. The `ip-approval-gate` workflow in
each project repo reads this repo on every pull request to `main` and
refuses the merge unless a record matches the PR's diff hash and is either
past its objection window or explicitly approved. Records are written by
`sandmill-infra/bin/ip-submit.sh`.
