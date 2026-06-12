# Local Model Offload Plan

The project should offload suitable planning/review tasks to local-only models. Do not use cloud escalation unless explicitly approved.

## Local endpoints

Switchboard:

```text
http://localhost:8002
```

Expert direct endpoint:

```text
http://localhost:8001
```

## Local-only rule

When using local model routing, pass local-only instructions explicitly.

Suggested prompt prefix:

```text
LOCAL ONLY. Do not escalate to cloud. If local execution is unavailable, return an error instead of escalating.
```

## Good offload tasks

- Review a single issue plan for missing steps.
- Generate shell command checklists from documentation.
- Review OCR algorithm pseudocode.
- Summarize logs from one failed test run.
- Suggest Tesseract parameter sweeps from a CSV failure report.

## Bad offload tasks

- Anything involving secrets.
- GitHub token or credential handling.
- Editing live Home Assistant compose files.
- Broad filesystem scans.
- Cloud escalation or Vertex/Gemini usage.

## Suggested execution pattern

1. Main orchestrator writes a narrow prompt file.
2. Send prompt to Switchboard on port 8002 with local-only constraint.
3. If task needs code reasoning and is still local-safe, send to 8001 directly.
4. Save outputs under `docs/local-model-notes/` only if useful.
5. Human/orchestrator reviews before applying changes.
