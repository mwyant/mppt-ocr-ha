"""Bootstrap GitHub labels, milestones, issues, and Projects v2 board.

Requires authenticated GitHub CLI (`gh`) with `repo` and `project` scopes.

Idempotent enough for project setup: existing labels, milestones, issues, and
project titles are reused when found.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any


OWNER = "mwyant"
REPO = "mppt-ocr-ha"
REPO_FULL = f"{OWNER}/{REPO}"
PROJECT_TITLE = "MPPT OCR HA"


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(args))
    return subprocess.run(args, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def gh_json(args: list[str]) -> Any:
    proc = run(args)
    return json.loads(proc.stdout or "null")


@dataclass(frozen=True)
class MilestoneDef:
    title: str
    description: str


@dataclass(frozen=True)
class IssueDef:
    title: str
    milestone: str
    labels: list[str]
    body: str


LABELS = {
    "type:docs": "0e8a16",
    "type:code": "1d76db",
    "type:infra": "5319e7",
    "type:test": "d4c5f9",
    "type:design": "fbca04",
    "priority:high": "b60205",
    "priority:medium": "d93f0b",
    "phase:foundation": "c2e0c6",
    "phase:streaming": "bfdadc",
    "phase:capture": "fef2c0",
    "phase:calibration": "c5def5",
    "phase:ocr": "f9d0c4",
    "phase:worker": "d4c5f9",
    "phase:deploy": "e99695",
    "phase:ha": "fef2c0",
}

MILESTONES = [
    MilestoneDef("M1 - Repository Safety and Project Skeleton", "Standalone repo, docs, safety boundaries, and runtime layout."),
    MilestoneDef("M2 - go2rtc Stream and Snapshot Service", "Camera stream and snapshot endpoint on Copernicus."),
    MilestoneDef("M3 - Snapshot Capture Harness", "Repeatable snapshot collection from go2rtc."),
    MilestoneDef("M4 - Image Calibration and Normalization", "Camera alignment, crop, perspective, and debug stages."),
    MilestoneDef("M5 - OCR and Template Evaluation", "Compare Tesseract and template/classical approaches against labeled samples."),
    MilestoneDef("M6 - Production Worker", "Validated 15-second OCR worker loop and local persistence."),
    MilestoneDef("M7 - Home Assistant Integration Later", "Publish stable stream/readings to HA after OCR is reliable."),
]

ISSUES = [
    IssueDef(
        "Create safe repository skeleton",
        "M1 - Repository Safety and Project Skeleton",
        ["type:docs", "priority:high", "phase:foundation"],
        """## Goal
Confirm this repository is standalone and safe to work in.

## Tasks
- Confirm repo exists at `mwyant/mppt-ocr-ha`.
- Confirm no project files modify the parent Home Assistant repo.
- Confirm no license file is added yet.
- Confirm planning docs exist for architecture, deployment, roadmap, and constraints.

## Acceptance
- `README.md` links all planning docs.
- `.gitignore` excludes runtime image/data artifacts.
- No existing HA stack files are touched.
""",
    ),
    IssueDef(
        "Define project-local runtime folder layout",
        "M1 - Repository Safety and Project Skeleton",
        ["type:docs", "priority:high", "phase:foundation"],
        """## Goal
Document the runtime folder structure under `/container_mounts/mppt-ocr-ha`.

## Tasks
- Define folders for go2rtc, OCR worker, logs, snapshots, debug artifacts, and results.
- Include explicit warning not to touch existing Home Assistant compose stacks.
- Include clone path recommendation.

## Acceptance
- `docs/COPERNICUS_DEPLOYMENT.md` has exact paths and commands.
        """,
    ),
    IssueDef(
        "Document and test local-only model offload workflow",
        "M1 - Repository Safety and Project Skeleton",
        ["type:docs", "priority:medium", "phase:foundation"],
        """## Goal
Make local-only model offload explicit and safe.

## Tasks
- Document Switchboard endpoint `localhost:8002`.
- Document direct Expert endpoint `localhost:8001`.
- Define prompt prefix requiring local-only execution.
- Identify safe offload tasks for mini/nano execution.
- Add a dry-run command or checklist that does not call cloud endpoints.

## Acceptance
- `docs/LOCAL_LLM_OFFLOAD.md` gives clear instructions for local-only task delegation.
- Project issues can reference the local-only workflow.
""",
    ),
    IssueDef(
        "Create isolated go2rtc compose/config scaffold",
        "M2 - go2rtc Stream and Snapshot Service",
        ["type:infra", "priority:high", "phase:streaming"],
        """## Goal
Create a project-local go2rtc deployment scaffold.

## Tasks
- Add `deploy/go2rtc/docker-compose.yml`.
- Add sample `deploy/go2rtc/go2rtc.yaml`.
- Map `/dev/video0` only inside this project-local compose.
- Document ports and LAN access.

## Acceptance
- `docker compose config` validates from the project folder.
- No existing compose file outside this repo is changed.
""",
    ),
    IssueDef(
        "Verify live stream endpoint on Copernicus",
        "M2 - go2rtc Stream and Snapshot Service",
        ["type:test", "priority:high", "phase:streaming"],
        """## Goal
Confirm go2rtc can stream the USB camera on Copernicus.

## Tasks
- Deploy go2rtc under `/container_mounts/mppt-ocr-ha/go2rtc`.
- Confirm container starts.
- Confirm stream page loads from LAN.
- Capture endpoint URLs in docs.

## Acceptance
- A documented URL serves live camera view.
- Logs show no camera device permission errors.
""",
    ),
    IssueDef(
        "Verify snapshot endpoint for OCR worker",
        "M2 - go2rtc Stream and Snapshot Service",
        ["type:test", "priority:high", "phase:streaming"],
        """## Goal
Confirm the OCR worker can fetch still frames from go2rtc.

## Tasks
- Confirm a snapshot URL returns a JPEG.
- Save one snapshot under project data folder.
- Record resolution and content type.

## Acceptance
- Snapshot fetch command is documented.
- Saved snapshot can be opened and inspected.
""",
    ),
    IssueDef(
        "Implement snapshot fetch CLI",
        "M3 - Snapshot Capture Harness",
        ["type:code", "priority:high", "phase:capture"],
        """## Goal
Create a small Python CLI that fetches a single go2rtc snapshot.

## Tasks
- Fetch one snapshot URL with timeout.
- Write image under `data/snapshots/`.
- Write JSON sidecar metadata with timestamp, URL, content type, and size.
- Log failures clearly.

## Acceptance
- CLI fetches one image from go2rtc and writes metadata.
""",
    ),
    IssueDef(
        "Implement interval capture mode",
        "M3 - Snapshot Capture Harness",
        ["type:code", "priority:medium", "phase:capture"],
        """## Goal
Collect calibration batches without cron.

## Tasks
- Add interval mode for repeated snapshots.
- Include `--count`, `--interval-seconds`, and output-dir args.
- Avoid overwriting existing files.

## Acceptance
- Can collect a labeled calibration batch from go2rtc snapshots.
""",
    ),
    IssueDef(
        "Add camera alignment guide",
        "M4 - Image Calibration and Normalization",
        ["type:docs", "priority:high", "phase:calibration"],
        """## Goal
Document physical camera alignment using the live go2rtc stream.

## Tasks
- Define good framing criteria: LCD fills frame, minimal parallax, no right-edge clipping, no bottom-button artifacts.
- Define bad framing examples.
- Document how to save calibration samples.

## Acceptance
- A human can reposition the camera using the live stream and the guide.
""",
    ),
    IssueDef(
        "Implement crop and perspective calibration config",
        "M4 - Image Calibration and Normalization",
        ["type:code", "priority:high", "phase:calibration"],
        """## Goal
Normalize snapshots before OCR.

## Tasks
- Add YAML/JSON config for crop rectangle.
- Add optional four-corner perspective correction.
- Add debug output for raw, cropped, warped, and thresholded frames.

## Acceptance
- One command processes a snapshot and writes all debug stages.
""",
    ),
    IssueDef(
        "Implement Tesseract host adapter",
        "M5 - OCR and Template Evaluation",
        ["type:code", "priority:high", "phase:ocr"],
        """## Goal
Use host-installed Tesseract on Copernicus.

## Tasks
- Detect host `tesseract` binary.
- Run OCR on a supplied crop.
- Capture stdout, stderr, exit code, and timing.
- Add numeric whitelist options.

## Acceptance
- Adapter can OCR a test crop on Copernicus.
""",
    ),
    IssueDef(
        "Implement Tesseract Docker adapter",
        "M5 - OCR and Template Evaluation",
        ["type:code", "priority:medium", "phase:ocr"],
        """## Goal
Use `jitesoft/tesseract-ocr` as an isolated test adapter.

## Tasks
- Run OCR using Docker image `jitesoft/tesseract-ocr`.
- Mount temp crop directory.
- Use same config as host adapter where possible.
- Warn that one-shot containers are test-only unless performance is acceptable.

## Acceptance
- Adapter works locally and on Copernicus Docker.
""",
    ),
    IssueDef(
        "Implement template-matching prototype",
        "M5 - OCR and Template Evaluation",
        ["type:code", "priority:high", "phase:ocr"],
        """## Goal
Create a CPU-only fallback that does not depend on Tesseract behavior.

## Tasks
- Segment digit-like components from labeled samples.
- Normalize crops to fixed size.
- Compare against templates with pixel distance.
- Use positional constraints for valid digits.

## Acceptance
- Prototype reports expected vs predicted CSV on labeled sample batch.
""",
    ),
    IssueDef(
        "Build OCR evaluation report CLI",
        "M5 - OCR and Template Evaluation",
        ["type:code", "priority:high", "phase:ocr"],
        """## Goal
Compare all recognition methods against labeled sample images.

## Tasks
- Run enabled adapters against a labeled folder.
- Parse expected values from filenames.
- Output CSV and summary stats.
- Save debug crops for failures.

## Acceptance
- Command reports top accuracy, bottom accuracy, and both-values accuracy.
""",
    ),
    IssueDef(
        "Implement validated OCR worker loop",
        "M6 - Production Worker",
        ["type:code", "priority:high", "phase:worker"],
        """## Goal
Run continuous validated readings every ~15 seconds.

## Tasks
- Poll snapshot endpoint on configured interval.
- Process image with selected adapter.
- Validate top and bottom ranges.
- Write latest result JSON and append history.
- Preserve invalid-read diagnostics.

## Acceptance
- Worker can run for 30 minutes and produce timestamped readings or explainable invalid reads.
""",
    ),
    IssueDef(
        "Add systemd service for OCR worker",
        "M6 - Production Worker",
        ["type:infra", "priority:medium", "phase:worker"],
        """## Goal
Run the OCR worker as a managed Copernicus service.

## Tasks
- Create systemd service template.
- Include environment/config path.
- Include restart policy.
- Document install, start, stop, and status commands.

## Acceptance
- Service starts and writes logs under project path.
""",
    ),
    IssueDef(
        "Decide HA publishing mechanism",
        "M7 - Home Assistant Integration Later",
        ["type:design", "priority:medium", "phase:ha"],
        """## Goal
Decide how stable readings should enter Home Assistant.

## Tasks
- Compare MQTT vs REST vs file sensor.
- Recommend one approach.
- Document HA config changes required.

## Acceptance
- Decision record exists before any HA config is touched.
""",
    ),
    IssueDef(
        "Add HA camera and sensor integration",
        "M7 - Home Assistant Integration Later",
        ["type:code", "priority:medium", "phase:ha"],
        """## Goal
Expose final stream and values in Home Assistant.

## Tasks
- Add HA camera entity for go2rtc stream.
- Add sensors for top and bottom values.
- Add availability and last-update fields.

## Acceptance
- HA shows live stream and validated numeric sensors.
""",
    ),
]


def ensure_labels() -> None:
    for name, color in LABELS.items():
        proc = run(["gh", "label", "create", name, "--color", color, "-R", REPO_FULL], check=False)
        if proc.returncode != 0 and "already exists" not in proc.stderr:
            raise RuntimeError(proc.stderr)


def ensure_milestones() -> dict[str, int]:
    existing = gh_json(["gh", "api", f"repos/{REPO_FULL}/milestones", "--paginate"])
    by_title = {m["title"]: m["number"] for m in existing}
    for ms in MILESTONES:
        if ms.title in by_title:
            continue
        created = gh_json([
            "gh",
            "api",
            f"repos/{REPO_FULL}/milestones",
            "-f",
            f"title={ms.title}",
            "-f",
            f"description={ms.description}",
        ])
        by_title[ms.title] = created["number"]
    return by_title


def ensure_issues(milestones: dict[str, int]) -> list[str]:
    existing = gh_json(["gh", "issue", "list", "-R", REPO_FULL, "--state", "all", "--limit", "200", "--json", "title,url"])
    by_title = {i["title"]: i["url"] for i in existing}
    urls: list[str] = []
    for issue in ISSUES:
        if issue.title in by_title:
            urls.append(by_title[issue.title])
            continue
        args = [
            "gh",
            "issue",
            "create",
            "-R",
            REPO_FULL,
            "--title",
            issue.title,
            "--body",
            issue.body,
            "--milestone",
            issue.milestone,
        ]
        for label in issue.labels:
            args.extend(["--label", label])
        proc = run(args)
        url = proc.stdout.strip().splitlines()[-1]
        urls.append(url)
    return urls


def ensure_project(issue_urls: list[str]) -> tuple[int, str]:
    projects = gh_json(["gh", "project", "list", "--owner", OWNER, "--format", "json", "--limit", "100"])
    project_number = None
    project_url = ""
    for p in projects.get("projects", []):
        if p.get("title") == PROJECT_TITLE:
            project_number = int(p["number"])
            project_url = p.get("url", "")
            break

    if project_number is None:
        created = gh_json(["gh", "project", "create", "--owner", OWNER, "--title", PROJECT_TITLE, "--format", "json"])
        project_number = int(created["number"])
        project_url = created.get("url", "")

    # Link repo; ignore if already linked.
    run(["gh", "project", "link", str(project_number), "--owner", OWNER, "--repo", REPO], check=False)

    current_items = gh_json(["gh", "project", "item-list", str(project_number), "--owner", OWNER, "--format", "json", "--limit", "200"])
    existing_urls = {item.get("content", {}).get("url") for item in current_items.get("items", [])}
    for url in issue_urls:
        if url in existing_urls:
            continue
        run(["gh", "project", "item-add", str(project_number), "--owner", OWNER, "--url", url], check=False)

    return project_number, project_url


def main() -> int:
    ensure_labels()
    milestones = ensure_milestones()
    urls = ensure_issues(milestones)
    number, url = ensure_project(urls)
    print(f"Created/updated {len(urls)} issues")
    print(f"Project: #{number} {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
