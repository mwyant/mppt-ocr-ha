# Camera Alignment Guide

This guide describes how to physically align the camera for optimal OCR performance.

## Goals

1.  **Fill the Frame:** The MPPT display should occupy as much of the frame as possible without clipping.
2.  **Minimize Parallax:** The camera should be as perpendicular to the display as possible.
3.  **No Clipping:** Ensure the right edge (where units like 'V' or 'A' might be) and the top/bottom edges of the digits are fully visible.
4.  **Avoid Artifacts:** Ensure the bottom buttons of the MPPT are not causing reflections or being detected as digits.
5.  **Stable Lighting:** Avoid direct glare on the LCD glass.

## Alignment Process

1.  Open the live stream: `http://copernicus:1984/stream.html?src=mppt`
2.  Physically adjust the camera mount.
3.  Verify the rotation is correct (should be 90 deg CCW if mounted sideways).
4.  Capture a test snapshot using the CLI:
    ```bash
    python3 src/capture_snapshot.py --out data/calibration
    ```
5.  Inspect the snapshot. If the digits are blurry or skewed, readjust.

## Good vs. Bad Framing

- **Good:** Digits are large, sharp, and level. High contrast between segments and background.
- **Bad:** Camera is at a sharp angle (trapezoidal distortion), digits are tiny in the center of a large frame, or segments are washed out by glare.
