# MPPT OCR HA: Project Status & Handover (June 12, 2026)

## 1. Executive Summary
The project has successfully established a robust image acquisition and vision-based OCR pipeline. We pivoted from brittle local template matching to a high-accuracy Gemini-based polling worker. The infrastructure is fully scaffolded but currently **OFFLINE** to prevent rate-limiting and resource drain during the next planning phase.

## 2. Technical Architecture
- **Image Source:** USB Camera on Copernicus (`/dev/video0`).
- **Streaming Service:** `go2rtc` (Docker) provides a live stream and a high-res snapshot endpoint.
- **OCR Worker:** A Python systemd service (`mppt-ocr.service`) running in a venv.
- **Vision Engine:** Gemini 1.5 Flash (via direct REST API) for robust digit recognition.
- **Persistence:** MariaDB (`mppt_db`) on Copernicus, accessed via a `socat` proxy container (`mppt-db-proxy`).

## 3. Current Implementation Details

### Active Components (Scaffolded)
- **`deploy/go2rtc/`**: Docker Compose for the stream service. Includes a 90-degree CCW rotation filter.
- **`deploy/db-proxy/`**: `socat` proxy to bridge the host/HA to the internal `romm-db` container on port `3307`.
- **`src/poll_gemini.py`**: The main worker. Features:
    - Direct REST calls using `AQ.` prefixed API keys.
    - Structured JSON output: `{"top": <int>, "bottom": <float>}`.
    - MariaDB integration (Table: `mppt_db.readings`).
    - Retry logic and 60s polling interval to respect rate limits.

### Credentials & Security
- **API Key:** Stored in `/container_mounts/mppt-ocr-ha/.secrets` (Line 1).
- **DB Password:** Stored in `/container_mounts/mppt-ocr-ha/.secrets` (Line 2).
- **DB User:** `mppt_user` authorized for `172.19.0.1` (Docker Bridge) and `10.1.3.11` (Home Assistant).

## 4. Known Issues & Blockers
1. **Rate Limiting (429):** The Gemini free tier is sensitive. The current 60s interval with retries is a mitigation, not a total fix.
2. **Database Table:** The `readings` table was failing to create/persist in the last run. Needs manual verification in MariaDB.
3. **Stream Rotation:** The `go2rtc` UI shows raw video; the rotation filter only applies to the API snapshots used by the worker.

## 5. Next Steps for the Next Agent
1. **Database Proof-of-Life:** Spin up `mppt-db-proxy`, verify `mppt_user` can connect, and ensure the `readings` table exists.
2. **Worker Resumption:** Restart `mppt-ocr.service` and monitor `journalctl -u mppt-ocr.service -f` for successful DB writes.
3. **HA Integration:** Configure the Home Assistant SQL Sensor to poll `10.1.3.13:3307`.
4. **MQTT Pivot:** (Optional) See Issue #20 for moving away from direct DB polling to an event-driven MQTT model.

## 6. Critical Paths
- **Local Repo:** `E:\build\home_infrastructure\mppt-ocr-ha`
- **Copernicus Root:** `/container_mounts/mppt-ocr-ha/`
- **MariaDB Host:** `172.19.0.3` (Internal) / `127.0.0.1:3307` (Via Proxy)
