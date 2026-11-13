#!/usr/bin/env python3
"""Pipeline status for every project under prior approval, from GitHub only.

For each project: the batch branch on the public staging mirror
(`release-candidate`) and its release-candidate checks, the latest record in
this repo (submitted / approved / objection / deemed approved), whether that
head has reached the canonical main, and the latest deploy runs on main.

    scripts/status.py               # terminal table
    scripts/status.py --markdown    # the table as markdown
    scripts/status.py --readme      # rewrite the README section (CI)

Needs `gh` authenticated (GH_TOKEN in CI). Everything it reads is public.
"""
import base64
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys

OWNER = "vthunder"
PROJECTS = ["browserid-ng", "mingo", "sbo", "browserid-pay", "browserid-bsky"]
BATCH_BRANCH = "release-candidate"
# Must pass on the mirror before submission, not required at merge
# (sandmill-infra/bin/ip-lib.sh ip_presubmit_only_checks; PLAN.md section 4).
PRESUBMIT_ONLY = {"sbo": ["rc / supply-chain"]}
PRESUBMIT_DEFAULT = ["rc / audit"]
# Projects that have no deploy workflow of their own.
DEPLOYS_ELSEWHERE = {"sbo": "via mingo (pinned SBO_REV)"}
# Advisory-ignore lists; every entry carries "Review: YYYY-MM-DD".
IGNORE_FILES = [".cargo/audit.toml", "deny.toml", ".github/supply-chain/npm-ignore.txt",
                ".github/supply-chain/pip-ignore.txt"]
REVIEW = re.compile(r"[Rr]eview(?: by)?:?\s*(\d{4}-\d{2}-\d{2})")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOW = dt.datetime.now(dt.timezone.utc)


def gh(path):
    env = dict(os.environ, CLICOLOR_FORCE="0", NO_COLOR="1")
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def parse_time(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def required_checks(project):
    prot = gh(f"repos/{OWNER}/{project}/branches/main/protection/required_status_checks") or {}
    names = {c for c in prot.get("contexts", []) if c != "ip-approval-gate"}
    if names:
        names |= set(PRESUBMIT_ONLY.get(project, PRESUBMIT_DEFAULT))
    return sorted(names)


def mirror_checks(project, sha, required):
    data = gh(f"repos/{OWNER}/{project}-staging/commits/{sha}/check-runs?per_page=100") or {}
    latest = {}
    for run in data.get("check_runs", []):
        latest.setdefault(run["name"], run)  # API lists newest first
    if not required:
        # Branch protection is readable only with admin rights (not by the
        # workflow token): count every release-candidate job on the commit,
        # which is the same set (each is required at merge or before submission).
        required = sorted(n for n in latest if n.startswith("rc / "))
    ok = failed = pending = 0
    bad = []
    for name in required:
        run = latest.get(name)
        if not run or run["status"] != "completed":
            pending += 1
        elif run["conclusion"] == "success":
            ok += 1
        else:
            failed += 1
            bad.append(name)
    return {"ok": ok, "failed": failed, "pending": pending, "total": len(required), "bad": bad}


def checks_text(c):
    if c["total"] == 0:
        return "no rc checks"
    if c["failed"]:
        return f"{c['failed']} failing ({', '.join(c['bad'])})"
    if c["pending"]:
        return f"{c['ok']}/{c['total']} green, {c['pending']} running"
    return f"{c['ok']}/{c['total']} green"


def in_main(project, sha):
    cmp = gh(f"repos/{OWNER}/{project}/compare/{sha}...main")
    return bool(cmp) and cmp.get("status") in ("ahead", "identical")


def latest_record(project):
    files = sorted(glob.glob(os.path.join(ROOT, "records", project, "*.json")))
    if not files:
        return None, None
    with open(files[-1]) as f:
        return json.load(f), os.path.relpath(files[-1], ROOT)


def record_state(rec):
    if rec.get("objection"):
        return "objection", "objection: " + str(rec["objection"])
    if rec.get("approved_at"):
        how = "exempt build-config" if rec.get("exempt") else "approved"
        return "approved", how + " " + rec["approved_at"][:10]
    due = parse_time(rec["submitted_at"]) + dt.timedelta(days=rec.get("wait_days", 14))
    if NOW >= due:
        return "approved", f"deemed approved {due:%Y-%m-%d}"
    days = (due - NOW).days + 1
    return "waiting", f"submitted {rec['submitted_at'][:10]}, deemed approved {due:%Y-%m-%d} ({days} d)"


def deploys(project):
    data = gh(f"repos/{OWNER}/{project}/actions/runs?branch=main&event=push&per_page=100") or {}
    latest = {}
    for run in data.get("workflow_runs", []):
        name = os.path.basename(run["path"])
        if name.startswith("deploy-"):
            latest.setdefault(name, run)
    if not latest:
        return DEPLOYS_ELSEWHERE.get(project, "no deploy runs")
    bad = [n for n, r in latest.items() if r["status"] == "completed" and r["conclusion"] != "success"]
    running = [n for n, r in latest.items() if r["status"] != "completed"]
    last = max(r["created_at"] for r in latest.values())[:10]
    if bad:
        return f"FAILED: {', '.join(bad)} (last {last})"
    if running:
        return f"running: {', '.join(running)}"
    return f"{len(latest)} ok, last {last}"


def ignore_reviews(project):
    """The earliest review date among main's advisory ignores: the trigger
    to re-evaluate them (upgrade, or extend with a new reason)."""
    dates = []
    for f in IGNORE_FILES:
        c = gh(f"repos/{OWNER}/{project}/contents/{f}?ref=main")
        if c and c.get("content"):
            dates += REVIEW.findall(base64.b64decode(c["content"]).decode("utf-8", "replace"))
    if not dates:
        return ""
    first = min(dates)
    if first <= f"{NOW:%Y-%m-%d}":
        return f"REVIEW DUE ({first})"
    return f"next review {first}"


def pending_disclosures():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "records", "*", "*.json"))):
        with open(f) as fh:
            r = json.load(fh)
        if r.get("disclose") and not r.get("disclosed_in"):
            out.append(f"{r['project']}: {r['disclose']} ([record]({os.path.relpath(f, ROOT)}))")
    return out


def local_stamp(project, sha):
    d = os.path.expanduser(f"~/ip-submissions/.verified/{project}/{sha}")
    return os.path.isfile(d)


def project_status(project):
    required = required_checks(project)
    main = gh(f"repos/{OWNER}/{project}/commits/main") or {}
    main_sha = main.get("sha", "")[:8]
    rec, rec_path = latest_record(project)
    branch = gh(f"repos/{OWNER}/{project}-staging/branches/{BATCH_BRANCH}")
    head = branch["commit"]["sha"] if branch else None

    row = {"project": project, "main": main_sha, "deploy": deploys(project), "record": rec_path,
           "ignores": ignore_reviews(project)}
    rec_head = rec["head"] if rec else None
    merged = bool(rec_head) and in_main(project, rec_head)

    if rec and not merged:
        state, text = record_state(rec)
        row["stage"] = {"objection": "OBJECTION", "approved": "ready to merge", "waiting": "awaiting approval"}[state]
        row["detail"] = text
        row["head"] = rec_head[:8]
        row["checks"] = checks_text(mirror_checks(project, rec_head, required))
    elif head and not in_main(project, head):
        c = mirror_checks(project, head, required)
        row["stage"] = "in progress"
        row["head"] = head[:8]
        row["checks"] = checks_text(c)
        row["detail"] = "not submitted" + (" (verified locally)" if local_stamp(project, head) else "")
    else:
        row["stage"] = "merged" if rec else "no batch"
        row["head"] = (rec_head or "")[:8]
        row["checks"] = ""
        row["detail"] = record_state(rec)[1] if rec else ""
    # Work on the batch branch beyond the submitted head (not allowed while waiting).
    if rec and not merged and head and head != rec_head:
        row["detail"] += f"; WARNING: {BATCH_BRANCH} has moved to {head[:8]}"
    return row


def terminal(rows):
    cols = [("project", "repo"), ("stage", "stage"), ("head", "head"), ("checks", "mirror checks"),
            ("detail", "approval"), ("main", "main"), ("deploy", "deploys"), ("ignores", "advisory ignores")]
    widths = {k: max(len(h), *(len(str(r.get(k, ""))) for r in rows)) for k, h in cols}
    print("  ".join(h.ljust(widths[k]) for k, h in cols))
    print("  ".join("-" * widths[k] for k, _ in cols))
    for r in rows:
        print("  ".join(str(r.get(k, "")).ljust(widths[k]) for k, _ in cols))
    for d in pending_disclosures():
        print("to disclose in the next submission:", re.sub(r" \(\[record\].*", "", d))


def markdown(rows):
    icon = {"merged": "✅", "ready to merge": "🟢", "awaiting approval": "⏳", "in progress": "🛠️",
            "OBJECTION": "⛔", "no batch": "·"}
    out = ["| repo | stage | head | mirror checks | approval | main | deploys | advisory ignores |",
           "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        p = r["project"]
        head = f"[`{r['head']}`](https://github.com/{OWNER}/{p}-staging/commit/{r['head']})" if r["head"] else ""
        main = f"[`{r['main']}`](https://github.com/{OWNER}/{p}/commits/main)" if r["main"] else ""
        rec = f" ([record]({r['record']}))" if r.get("record") else ""
        deploy = f"[{r['deploy']}](https://github.com/{OWNER}/{p}/actions)"
        out.append(f"| [{p}](https://github.com/{OWNER}/{p}) | {icon.get(r['stage'], '')} {r['stage']} | {head} "
                   f"| {r['checks']} | {r['detail']}{rec} | {main} | {deploy} | {r['ignores']} |")
    disc = pending_disclosures()
    if disc:
        out += ["", "To mention in the next submission email:", ""] + [f"- {d}" for d in disc]
    return "\n".join(out)


START, END = "<!-- status:start -->", "<!-- status:end -->"


def update_readme(table):
    """Splice the table into README.md between the markers. The timestamp
    changes only when the table does, so an unchanged run commits nothing."""
    path = os.path.join(ROOT, "README.md")
    text = open(path).read()
    if START not in text:
        text = text.rstrip() + "\n\n## Status\n\n" + START + "\n" + END + "\n"
    before, rest = text.split(START, 1)
    old, after = rest.split(END, 1)
    if table in old:
        return
    stamp = f"Last change {NOW:%Y-%m-%d %H:%M} UTC; checked every 30 minutes by `.github/workflows/status.yml` (`scripts/status.py`)."
    with open(path, "w") as f:
        f.write(f"{before}{START}\n{table}\n\n{stamp}\n{END}{after}")


def main():
    rows = [project_status(p) for p in PROJECTS]
    if "--readme" in sys.argv:
        update_readme(markdown(rows))
    elif "--markdown" in sys.argv:
        print(markdown(rows))
    else:
        terminal(rows)


if __name__ == "__main__":
    main()
