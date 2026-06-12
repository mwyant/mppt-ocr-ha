# Implementation Roadmap

This roadmap is written so a smaller execution model can work issue-by-issue without needing to infer the whole system.

## Milestone 1: Repository and deployment skeleton

Goal: create a safe standalone project with no accidental coupling to existing HA stacks.

Deliverables:

- repo created at `mwyant/mppt-ocr-ha`
- local folder `./mppt-ocr-ha`
- remote clone under `/container_mounts/mppt-ocr-ha/repo` or similar
- documented folder layout
- no license initially

## Milestone 2: go2rtc camera stream and snapshots

Goal: replace cron/fswebcam capture with stream/snapshot service.

Deliverables:

- `go2rtc` config under `/container_mounts/mppt-ocr-ha/go2rtc/`
- isolated compose file under project path only
- live stream reachable on Copernicus LAN
- snapshot endpoint returns a current frame
- documented camera device path and permissions

## Milestone 3: Snapshot capture harness

Goal: save repeatable samples from go2rtc snapshots.

Deliverables:

- Python CLI to fetch one snapshot
- Python CLI to collect snapshots on interval
- output folders under `/container_mounts/mppt-ocr-ha/data/`
- metadata sidecars with timestamp, URL, and capture parameters

## Milestone 4: Image normalization and calibration

Goal: make OCR input stable before attempting value extraction.

Deliverables:

- calibration config for crop and optional four-corner perspective correction
- debug mode that saves raw, cropped, warped, thresholded images
- camera alignment guide using go2rtc live view
- baseline sample set collected after physical camera alignment

## Milestone 5: OCR/template evaluation harness

Goal: compare candidate recognition methods on labeled samples.

Deliverables:

- Tesseract-host adapter
- Tesseract-docker adapter using `jitesoft/tesseract-ocr`
- template-match prototype
- CSV report with expected vs predicted values
- debug artifacts for failures

## Milestone 6: Production OCR worker

Goal: run every ~15 seconds and emit validated readings.

Deliverables:

- worker config file
- structured logs
- local result store: SQLite or CSVL
- invalid-read handling policy
- service definition: systemd preferred for worker

## Milestone 7: Copernicus deployment automation

Goal: reproducible remote setup.

Deliverables:

- install script or documented command list
- service startup/stop commands
- health checks
- rollback procedure

## Milestone 8: Home Assistant integration, later

Goal: publish stable readings to HA only after OCR is reliable.

Deliverables:

- MQTT or REST publishing decision
- HA sensor definitions
- HA camera entity using go2rtc stream
- dashboard card optional
