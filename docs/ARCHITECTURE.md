# Architecture

## Summary

The project should be redesigned around image acquisition stability first. Previous attempts failed because the OCR code was forced to compensate for camera angle, partial clipping, bottom-button artifacts, and inconsistent digit segmentation.

The pipeline should therefore be layered:

1. Stream/capture reliability.
2. Snapshot consistency.
3. Image normalization.
4. Numeric region detection.
5. OCR/template classification.
6. Validation and persistence.
7. Home Assistant publication.

## Target runtime architecture

```text
Copernicus USB camera
  |
  v
go2rtc container
  |-- live stream for alignment/debug
  |-- snapshot endpoint for OCR worker
  v
OCR worker service
  |-- fetch snapshot every N seconds
  |-- save raw/debug sample optionally
  |-- normalize/perspective-correct
  |-- detect digit rows/components
  |-- classify values
  |-- validate hard ranges
  |-- store latest + history
  v
Later phase: MQTT/Home Assistant sensor publishing
```

## go2rtc responsibilities

go2rtc is responsible only for camera access and stream/snapshot serving.

Responsibilities:

- Own `/dev/video0` access where possible.
- Serve a live stream for camera positioning.
- Provide a snapshot URL for OCR worker polling.
- Run isolated under `/container_mounts/mppt-ocr-ha/go2rtc/`.

Non-responsibilities:

- OCR.
- Value validation.
- Database writes.
- Home Assistant entity state.

## OCR worker responsibilities

The OCR worker is a separate process. It may be a systemd service or later a container, but phase 1 should favor direct Python/systemd because it is easier to debug on Copernicus.

Responsibilities:

- Poll snapshot endpoint.
- Store controlled debug samples.
- Apply configurable preprocessing.
- Run digit detection/classification.
- Validate ranges.
- Write local result records.

## OCR engine strategy

The worker must expose an adapter interface so the OCR/classifier can be changed without rewriting capture logic.

Supported adapters to plan for:

1. `tesseract-host`
   - Calls `/usr/bin/tesseract` installed on Copernicus.
   - Preferred for production if accuracy is acceptable.
   - Fastest process startup.

2. `tesseract-docker`
   - Calls `jitesoft/tesseract-ocr` container.
   - Useful for dependency parity with local testing.
   - Slower if launching one container per crop; acceptable for test harness, not ideal for production.

3. `template-match`
   - CPU-only classical image matching.
   - Likely best long-term if the display font is stable.
   - Uses labeled samples to build digit templates.

## Processing strategy

Avoid brittle fixed character positions. Use this order:

1. Get stable snapshot.
2. Crop/normalize display region.
3. Optionally perspective-correct the display plane.
4. Threshold to foreground mask.
5. Detect digit-like components or row bands.
6. Group into top/bottom rows.
7. Classify digits or OCR row crops.
8. Use hard numeric constraints to accept/reject.

## Why not put OCR inside Home Assistant first?

Home Assistant should not own experimental OCR logic. Keep HA clean until the measurement pipeline is stable.

HA integration should be delayed until:

- go2rtc live stream works;
- snapshot endpoint works;
- OCR worker can produce valid top/bottom values over a sample window;
- debug artifacts can explain failures.
