# Operational Constraints

## Hard paths

Local development repo:

```text
./mppt-ocr-ha/
```

Copernicus runtime root:

```text
/container_mounts/mppt-ocr-ha/
```

All project runtime subfolders must live under that path, for example:

```text
/container_mounts/mppt-ocr-ha/go2rtc/
/container_mounts/mppt-ocr-ha/ocr-worker/
/container_mounts/mppt-ocr-ha/data/
/container_mounts/mppt-ocr-ha/logs/
```

## Do not touch

Do not edit existing unrelated Home Assistant compose files, dashboards, backups, or containers.

## Value constraints

Top display value:

- numeric integer
- valid range: `50 <= top <= 100`
- visible layout normally has two digit positions
- rare case: `100` may appear

Bottom display value:

- one decimal place
- valid range: `0.0 <= bottom <= 5.1`
- expected format: `D.D`
- current samples mostly below `2.2`

Digit-position constraints:

- top left component: normally `5-9`, rare `10` when top is `100`
- top right component: `0-9`
- bottom left component: `0-5`
- bottom right component: `0-9`

## Compute constraints

- All production processing runs on Copernicus.
- CPU-only is the default.
- GPU is not assumed.
- Cadence target: about every 15 seconds.
- OCR/runtime should be cheap enough to run continuously.

## Model routing constraints

- Use local-only model routing for planning or code review offload.
- Switchboard endpoint: `http://localhost:8002`
- Expert endpoint: `http://localhost:8001`
- Do not escalate to Gemini/Vertex unless explicitly approved.
