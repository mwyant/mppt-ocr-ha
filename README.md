# MPPT OCR HA

CPU-first MPPT display capture, streaming, OCR, and Home Assistant publishing pipeline for Copernicus.

This repository is intentionally scoped away from the existing Home Assistant stack. Runtime files on Copernicus belong under:

```text
/container_mounts/mppt-ocr-ha/
```

No existing HA Docker Compose files should be edited by this project.

## Project goal

Read two live values from a camera pointed at an MPPT/controller display:

- Top value: integer range `50-100`
- Bottom value: one-decimal range `0.0-5.1`

Eventually publish these values to Home Assistant, but only after the streaming and snapshot/OCR pipeline works reliably.

## Recommended runtime architecture

```text
USB camera on Copernicus
  -> go2rtc container
  -> live stream + snapshot endpoint
  -> OCR worker on Copernicus
  -> local validation/store
  -> later: MQTT/Home Assistant sensors
```

## Current design decision

Use a hybrid deployment:

- `go2rtc` runs in Docker for streaming/snapshot service.
- OCR worker runs as local Python/systemd first, using either:
  - host-installed `tesseract`, preferred for speed and simplicity on Copernicus, or
  - `jitesoft/tesseract-ocr` container if dependency isolation matters.

The implementation must support both modes behind one OCR adapter.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Implementation Roadmap](docs/ROADMAP.md)
- [Issue Plan](docs/ISSUE_PLAN.md)
- [Copernicus Deployment](docs/COPERNICUS_DEPLOYMENT.md)
- [Local Model Offload Plan](docs/LOCAL_LLM_OFFLOAD.md)
- [Operational Constraints](docs/CONSTRAINTS.md)

## Non-goals for phase 1

- Home Assistant entity publishing
- Dashboard design
- Existing HA stack modifications
- Long-term database schema beyond local CSV/SQLite proof-of-life

Those come after streaming + snapshots + OCR are stable.
