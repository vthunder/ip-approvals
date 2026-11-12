# Build configuration: no prior approval needed

In the 2026-11-08 submission email Dan asked Avail to confirm:

> I don't think changes like these count as code developed under the
> clause, but I'd like to confirm that: version numbers of my own packages,
> pinned versions of the compiler, base images and CI actions, dependency
> updates for upstream security fixes, and CI/deployment configuration.
> Anything with program logic I'll keep submitting as before.

Avail replied "Approved" (reported by Dan on 2026-11-12).

Changes of that kind are recorded here with `"exempt": "build-config"`
and `"basis": "policy/build-config.md"`, approved when recorded. Each one
must pass `sandmill-infra/bin/ip-exempt-check.py`, which accepts only
lockfiles, CI and deployment configuration, and manifest changes limited
to version strings, revs and toolchain pins. Anything else, including any
change to source code, scripts, vendored code or tests, goes through the
normal two-week route.
