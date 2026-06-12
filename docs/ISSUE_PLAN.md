# GitHub Issue Plan

These are the planned GitHub issues and milestones. Each issue is intentionally scoped for a small execution model.

## Milestone: M1 - Repository Safety and Project Skeleton

### Issue: Create safe repository skeleton

Labels: `type:docs`, `priority:high`, `phase:foundation`

Tasks:

- Confirm repo exists at `mwyant/mppt-ocr-ha`.
- Confirm no project files modify parent Home Assistant repo.
- Confirm no license file is added yet.
- Confirm documentation exists for architecture, deployment, roadmap, and constraints.

Acceptance:

- `README.md` links all planning docs.
- `.gitignore` excludes runtime image/data artifacts.

### Issue: Define project-local runtime folder layout

Labels: `type:docs`, `priority:high`, `phase:foundation`

Tasks:

- Document `/container_mounts/mppt-ocr-ha` layout.
- Define where go2rtc, OCR worker, logs, and data live.
- Include explicit warning not to touch existing HA compose stacks.

Acceptance:

- `docs/COPERNICUS_DEPLOYMENT.md` has exact paths and commands.

### Issue: Document and test local-only model offload workflow

Labels: `type:docs`, `priority:medium`, `phase:foundation`

Tasks:

- Document Switchboard endpoint `localhost:8002`.
- Document direct Expert endpoint `localhost:8001`.
- Define prompt prefix requiring local-only execution.
- Identify safe offload tasks for mini/nano execution.
- Add a dry-run command or checklist that does not call cloud endpoints.

Acceptance:

- `docs/LOCAL_LLM_OFFLOAD.md` gives clear instructions for local-only task delegation.
- Project issues can reference the local-only workflow.

## Milestone: M2 - go2rtc Stream and Snapshot Service

### Issue: Create isolated go2rtc compose/config scaffold

Labels: `type:infra`, `priority:high`, `phase:streaming`

Tasks:

- Add project-local `deploy/go2rtc/docker-compose.yml`.
- Add sample `go2rtc.yaml` config.
- Map `/dev/video0` only inside project-local compose.
- Document ports and LAN access.

Acceptance:

- `docker compose config` validates from the project folder.
- No existing compose file outside project is changed.

### Issue: Verify live stream endpoint on Copernicus

Labels: `type:test`, `priority:high`, `phase:streaming`

Tasks:

- Deploy go2rtc on Copernicus.
- Confirm container starts.
- Confirm stream page loads from LAN.
- Capture endpoint URLs.

Acceptance:

- A documented URL serves live camera view.
- Logs show no camera device permission errors.

### Issue: Verify snapshot endpoint for OCR worker

Labels: `type:test`, `priority:high`, `phase:streaming`

Tasks:

- Confirm a snapshot URL returns a JPEG.
- Save one snapshot under project data folder.
- Record resolution and content type.

Acceptance:

- Snapshot fetch command is documented.
- Saved snapshot can be opened and inspected.

## Milestone: M3 - Snapshot Capture Harness

### Issue: Implement snapshot fetch CLI

Labels: `type:code`, `priority:high`, `phase:capture`

Tasks:

- Create Python CLI to fetch one snapshot URL.
- Write output to `data/snapshots/`.
- Write JSON sidecar metadata.
- Add timeout and failure logging.

Acceptance:

- CLI fetches one image from go2rtc and writes metadata.

### Issue: Implement interval capture mode

Labels: `type:code`, `priority:medium`, `phase:capture`

Tasks:

- Add interval mode for repeated snapshots.
- Include max count and delay args.
- Avoid overwriting existing files.

Acceptance:

- Can collect a labeled calibration batch without cron.

## Milestone: M4 - Image Calibration and Normalization

### Issue: Add camera alignment guide

Labels: `type:docs`, `priority:high`, `phase:calibration`

Tasks:

- Document physical camera alignment goals.
- Include examples of good/bad framing.
- Prioritize LCD filling frame, minimal parallax, no right-edge clipping, no bottom-button artifacts.

Acceptance:

- A human can reposition camera using go2rtc live view.

### Issue: Implement crop and perspective calibration config

Labels: `type:code`, `priority:high`, `phase:calibration`

Tasks:

- Add YAML/JSON config for crop rectangle.
- Add optional four-corner perspective correction.
- Add debug output for raw/cropped/warped/thresholded frames.

Acceptance:

- One command processes a snapshot and writes debug stages.

## Milestone: M5 - OCR and Template Evaluation

### Issue: Implement Tesseract host adapter

Labels: `type:code`, `priority:high`, `phase:ocr`

Tasks:

- Detect host `tesseract` binary.
- Run OCR on a supplied crop.
- Capture stdout/stderr and timing.
- Add numeric whitelist options.

Acceptance:

- Adapter can OCR a test crop on Copernicus.

### Issue: Implement Tesseract Docker adapter

Labels: `type:code`, `priority:medium`, `phase:ocr`

Tasks:

- Use `jitesoft/tesseract-ocr` image.
- Mount temp crop directory read-only if possible.
- Run OCR with same config as host adapter.
- Warn that one-shot containers are test-only unless performance is acceptable.

Acceptance:

- Adapter works locally and on Copernicus Docker.

### Issue: Implement template-matching prototype

Labels: `type:code`, `priority:high`, `phase:ocr`

Tasks:

- Segment digit-like components from labeled samples.
- Normalize crops to fixed size.
- Compare against templates with pixel distance.
- Use positional constraints for valid digits.

Acceptance:

- Prototype reports expected vs predicted CSV on labeled sample batch.

### Issue: Build OCR evaluation report CLI

Labels: `type:code`, `priority:high`, `phase:ocr`

Tasks:

- Run all enabled adapters against a labeled folder.
- Parse expected values from filenames.
- Output CSV and summary stats.
- Save debug crops for failures.

Acceptance:

- Command reports top accuracy, bottom accuracy, and both-values accuracy.

## Milestone: M6 - Production Worker

### Issue: Implement validated OCR worker loop

Labels: `type:code`, `priority:high`, `phase:worker`

Tasks:

- Poll snapshot endpoint every configured interval.
- Process image with chosen adapter.
- Validate top and bottom ranges.
- Write latest result JSON and append history.

Acceptance:

- Worker can run for 30 minutes and produce timestamped readings or explainable invalid reads.

### Issue: Add systemd service for OCR worker

Labels: `type:infra`, `priority:medium`, `phase:worker`

Tasks:

- Create service file template.
- Include environment/config path.
- Include restart policy.
- Document install/start/stop/status commands.

Acceptance:

- Service starts and writes logs under project path.

## Milestone: M7 - Home Assistant Integration Later

### Issue: Decide HA publishing mechanism

Labels: `type:design`, `priority:medium`, `phase:ha`

Tasks:

- Compare MQTT vs REST vs file sensor.
- Recommend one approach.
- Document HA config changes required.

Acceptance:

- Decision record exists before any HA config is touched.

### Issue: Add HA camera and sensor integration

Labels: `type:code`, `priority:medium`, `phase:ha`

Tasks:

- Add HA camera entity for go2rtc stream.
- Add sensors for top and bottom values.
- Add availability/last-update fields.

Acceptance:

- HA shows live stream and validated numeric sensors.
