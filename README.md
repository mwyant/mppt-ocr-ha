# MPPT OCR HA

CPU-first MPPT display capture, streaming, OCR, and Home Assistant publishing pipeline for Copernicus.

This repository is intentionally scoped away from the existing Home Assistant stack. Runtime files on Copernicus belong under:

```text
/container_mounts/mppt-ocr-ha/
```

No existing HA Docker Compose files should be edited by this project.

## Project Goal

Read two live values from a camera pointed at an MPPT/controller display:
- **Top value:** integer range `50-100`
- **Bottom value:** one-decimal range `0.0-5.1`

## Current Status (Milestones 1-5 Complete)

- **Streaming:** `go2rtc` is running on Copernicus via Docker Compose.
- **Capture:** Python CLI `src/capture_snapshot.py` is ready for interval-based data collection.
- **Calibration:** `src/calibrate_image.py` handles cropping and thresholding.
- **OCR:** `src/ocr_adapters.py` and `src/evaluate_ocr.py` are ready for accuracy testing.

## Quick Start for AI Agents / Human Workers

### 1. Environment Setup
- **Local Repo:** `E:\build\home_infrastructure\mppt-ocr-ha`
- **Copernicus Repo:** `/container_mounts/mppt-ocr-ha/repo`
- **Copernicus Runtime:** `/container_mounts/mppt-ocr-ha/go2rtc`
- **Endpoints:**
  - Live Stream: [http://copernicus:1984/stream.html?src=mppt](http://copernicus:1984/stream.html?src=mppt)
  - Snapshot API: [http://copernicus:1984/api/frame.jpeg?src=mppt](http://copernicus:1984/api/frame.jpeg?src=mppt)

### 2. Data Collection & Labeling
To collect samples for OCR training/evaluation:
```bash
# On Copernicus
python3 src/capture_snapshot.py --out data/samples --count 10 --interval 5
```
Manually rename files to `<value>_<position>_<timestamp>.jpg` (e.g., `52.1_bottom_123.jpg`).

### 3. Calibration
Adjust `config/calibration.json` to define the crop area and threshold. Test with:
```bash
python3 src/calibrate_image.py data/samples/sample.jpg --config config/calibration.json --out debug_cal/test
```

### 4. Evaluation
Run the evaluation suite to check OCR accuracy:
```bash
python3 src/evaluate_ocr.py data/labeled_samples --out results.csv
```

## Documentation Index

- [Architecture](docs/ARCHITECTURE.md) - System design and data flow.
- [Implementation Roadmap](docs/ROADMAP.md) - Milestone tracking.
- [Issue Plan](docs/ISSUE_PLAN.md) - Detailed task breakdowns.
- [Copernicus Deployment](docs/COPERNICUS_DEPLOYMENT.md) - Remote paths and commands.
- [Alignment Guide](docs/ALIGNMENT_GUIDE.md) - Physical camera positioning.
- [Operational Constraints](docs/CONSTRAINTS.md) - Hard boundaries for the project.
- [Local Model Offload Plan](docs/LOCAL_LLM_OFFLOAD.md) - How to use local AI for development.

## Non-goals for Phase 1
- Modifying existing HA stack.
- MQTT/Sensor publishing (comes in Milestone 8).
- Long-term database schema.
