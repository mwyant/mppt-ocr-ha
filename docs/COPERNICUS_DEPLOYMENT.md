# Copernicus Deployment Plan

## Runtime root

All runtime files belong under:

```text
/container_mounts/mppt-ocr-ha/
```

Recommended layout:

```text
/container_mounts/mppt-ocr-ha/
  repo/                    # git clone
  go2rtc/
    config/
    data/
    logs/
  ocr-worker/
    config/
    logs/
  data/
    snapshots/
    raw/
    normalized/
    debug/
    results/
```

## Git clone path

Recommended:

```text
/container_mounts/mppt-ocr-ha/repo
```

Commands:

```bash
cd /container_mounts/mppt-ocr-ha
git clone https://github.com/mwyant/mppt-ocr-ha.git repo
```

## go2rtc deployment shape

Use project-local compose only:

```text
/container_mounts/mppt-ocr-ha/go2rtc/docker-compose.yml
```

Do not edit any existing Home Assistant compose files.

go2rtc should be configured to expose:

- stream endpoint for viewing/camera alignment
- snapshot endpoint for OCR worker

## OCR deployment shape

Phase 1 worker should run as Python + systemd for easier debugging.

Potential service name:

```text
mppt-ocr-worker.service
```

## Tesseract decision

Prefer host-installed Tesseract on Copernicus if available:

```bash
command -v tesseract
tesseract --version
```

If host install is missing or inconsistent, use Docker adapter:

```bash
docker run --rm --entrypoint tesseract jitesoft/tesseract-ocr --version
```

Production caution: launching one container per OCR crop is slower. If Docker OCR is required in production, design a long-running OCR service/container instead of repeated one-shot containers.

## Permissions

Camera access may require group membership or device mapping.

Check:

```bash
ls -l /dev/video*
groups izzy_ai
```

If go2rtc runs in Docker, the compose file may need:

```yaml
devices:
  - /dev/video0:/dev/video0
```

## Health checks

Minimum health checks:

- go2rtc process/container running
- stream endpoint reachable
- snapshot endpoint returns image/jpeg
- OCR worker can fetch snapshot
- OCR worker writes latest result file
