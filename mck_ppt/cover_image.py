# Copyright 2024-2026 Kaku Li (https://github.com/likaku)
# Licensed under the Apache License, Version 2.0 — see LICENSE and NOTICE.
# Originally part of "Mck-ppt-design-skill" (McKinsey PPT Design Framework).
# NOTICE: This file must be retained in all copies or substantial portions.
#
# Adapted 2026 for "MBB PPT Generator":
#   - All Chinese subject prompts and metaphor keys translated to English.
#   - NegativePrompt translated to English.
#   - Console messages translated to English.
#   - Functionality unchanged: Tencent Hunyuan 2.0 API still used as the
#     image-generation backend. The Hunyuan API accepts English prompts.
#
"""Cover Image Generator — Tencent Hunyuan API + rembg cutout + cool grey-blue tint + ribbon decoration.

Output: 1920×1080 RGBA PNG with a transparent-background subject and full-bleed
geometric ribbon overlay, suitable for use as a full-frame backing layer on a
PPT cover slide.

Opt-in only. Disabled by default per the skill's security posture; users must
explicitly pass cover_image='auto' to eng.cover() AND set Tencent credentials
in environment variables to enable cloud image generation.

Usage:
    from mck_ppt.cover_image import generate_cover_image
    path = generate_cover_image('AI capability boundaries', output_path='cover.png')
"""

from __future__ import annotations

import base64
import json
import math
import os
import tempfile
import time
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from rembg import remove as rembg_remove

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models


# ── Theme keyword → physical subject prompt ─────────────────────────────
# The map keys are matched as substrings against the slide title (lowercased).
# Prompts describe a single, well-lit physical object — the goal is a clean
# studio-style product photo that can be cut out and placed on the cover.
_METAPHOR_MAP = {
    'ai':           'a high-end gaming graphics card with thick heatsink armor, RGB light strip, silver-and-black finish, 45-degree top-down angle',
    'artificial intelligence': 'a high-end gaming graphics card with thick heatsink armor, RGB light strip, silver-and-black finish, 45-degree top-down angle',
    'random':       'three polished metal dice, silver finish, arranged at a 45-degree angle',
    'data':         'an M.2 solid-state drive, black PCB with gold contact pins',
    'security':     'a modern smart deadbolt lock, silver metal faceplate, minimalist design',
    'medical':      'a silver stethoscope with a few colorful capsule pills',
    'pharma':       'a silver stethoscope with a few colorful capsule pills',
    'finance':      'a brushed-silver metal credit card with chip, 45-degree angle',
    'banking':      'a brushed-silver metal credit card with chip, 45-degree angle',
    'education':    'a silver laptop, partially open, side view',
    'energy':       'a deep-blue solar panel, top-down angle',
    'architecture': 'a white 3D-printed architectural building model, modern style',
    'tech':         'a square chip package with silver metal lid, top-down angle',
    'innovation':   'a white VR headset, side view',
    'strategy':     'a silver metal chess king piece',
    'platform':     'colorful Lego bricks assembled together',
    'digital':      'a smart watch with a circular dial and silver band',
    'chip':         'a square chip package with silver metal lid, top-down angle',
    'brain':        'a transparent resin model of a human brain on a base',
    'neural':       'a transparent resin model of a human brain on a base',
    'creativity':   'a few scattered colorful marker pens',
    'algorithm':    'a 3x3 Rubik\'s cube, predominantly white',
    'compute':      'a high-end gaming graphics card with thick heatsink armor, silver-and-black finish',
    'robot':        'a close-up of a single white robotic arm joint',
    'cloud':        'a silver Mac Mini, front view',
}

_PROMPT_TEMPLATE = (
    "Professional product photography, {object_desc}, "
    "pure white background, sharp clean outline, "
    "studio lighting, ultra-high definition"
)


def _find_metaphor(title: str) -> str:
    """Look up an English keyword in the title and return the corresponding
    subject prompt. Falls back to a neutral metal-sculpture image if no
    keyword matches."""
    title_lower = title.lower()
    for keyword, metaphor in _METAPHOR_MAP.items():
        if keyword in title_lower:
            return metaphor
    return 'a silver metal geometric sculpture'


def _build_prompt(title: str) -> str:
    return _PROMPT_TEMPLATE.format(object_desc=_find_metaphor(title))


# ═══════════════════════════════════════════════════════════════════════
# Post-processing
# ═══════════════════════════════════════════════════════════════════════

def _professional_remove_bg(img: Image.Image) -> Image.Image:
    """rembg cutout — keeps only the subject."""
    return rembg_remove(img).convert('RGBA')


def _apply_cool_blue_tint(img: Image.Image) -> Image.Image:
    """Cool grey-blue tint at 50% lightening; only affects non-transparent pixels."""
    img = img.convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    alpha = arr[:, :, 3]
    mask = alpha > 10

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    gray = 0.299 * r + 0.587 * g + 0.114 * b
    sat = 0.30
    r_new = (gray + (r - gray) * sat) * 0.85 * 0.5 + 255.0 * 0.5
    g_new = (gray + (g - gray) * sat) * 0.92 * 0.5 + 255.0 * 0.5
    b_new = np.minimum((gray + (b - gray) * sat) * 1.18, 255.0) * 0.5 + 255.0 * 0.5

    arr[:, :, 0][mask] = np.clip(r_new[mask], 0, 255)
    arr[:, :, 1][mask] = np.clip(g_new[mask], 0, 255)
    arr[:, :, 2][mask] = np.clip(b_new[mask], 0, 255)

    return Image.fromarray(arr.astype(np.uint8))


def _place_subject_right(subject: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    """Place the cut-out subject on the right side of the canvas.

    Subject occupies ~66% of canvas height and ~42% of canvas width,
    positioned slightly above center on the right side.
    """
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

    bbox = subject.getbbox()
    if not bbox:
        return canvas
    cropped = subject.crop(bbox)
    cw, ch = cropped.size

    # Subject scaled to ~66% of canvas height
    target_h = int(canvas_h * 0.66)
    scale = target_h / ch
    target_w = int(cw * scale)
    # Width cap at 42%
    if target_w > int(canvas_w * 0.42):
        target_w = int(canvas_w * 0.42)
        scale = target_w / cw
        target_h = int(ch * scale)

    resized = cropped.resize((target_w, target_h), Image.LANCZOS)

    # Position: slightly inset from the right edge, biased toward the upper half
    x = canvas_w - target_w + int(target_w * 0.05) - int(canvas_w * 0.10)
    y = canvas_h - target_h + int(target_h * 0.05) - int(canvas_h * 0.18)
    canvas.paste(resized, (x, y), resized)

    return canvas


def _draw_ribbon_curves(img: Image.Image) -> Image.Image:
    """Decorative ribbon curves — parallel lines that fold and twist at center.

    A bundle of parallel lines flows in from the lower-left, twists at the
    center of the canvas (lines on top cross to the bottom and vice versa),
    then fans out toward the upper right. Visually resembles a folded silk
    ribbon.
    """
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    w, h = img.size

    n_lines = 24
    for i in range(n_lines):
        # Normalize each line's index to [-1, 1]
        t = (i - (n_lines - 1) / 2.0) / ((n_lines - 1) / 2.0)

        center_dist = abs(t)
        alpha = int(105 * (1.0 - center_dist * 0.6))
        line_w = 2 if center_dist < 0.5 else 1
        color = (55, 105, 165, alpha)

        spread = t * h * 0.20  # vertical offset per line

        points = []
        n_seg = 300
        for s in range(n_seg + 1):
            frac = s / n_seg

            # Base path: lower-left → center → upper-right (cubic Bezier)
            p0x, p0y = w * 0.00, h * 1.05
            p1x, p1y = w * 0.30, h * 0.50
            p2x, p2y = w * 0.70, h * 0.50
            p3x, p3y = w * 1.00, h * -0.05

            u = 1 - frac
            bx = u**3*p0x + 3*u**2*frac*p1x + 3*u*frac**2*p2x + frac**3*p3x
            by = u**3*p0y + 3*u**2*frac*p1y + 3*u*frac**2*p2y + frac**3*p3y

            # Ribbon fold: gentle twist at center; tanh slope of 5.0 keeps
            # the transition soft (a slope of 12.0 was tried and felt too abrupt)
            twist = math.tanh((frac - 0.50) * 5.0)

            offset_y = spread * twist

            # Lines slightly converge at the fold but never fully overlap
            tightness = 1.0 - 0.20 * math.exp(-((frac - 0.50) ** 2) / (2 * 0.06 ** 2))
            offset_y *= tightness

            points.append((bx, by + offset_y))

        for j in range(len(points) - 1):
            draw.line([points[j], points[j + 1]], fill=color, width=line_w)

    return Image.alpha_composite(img, overlay)


def _post_process(image_path: str) -> str:
    """Post-processing pipeline:
    1. rembg cutout
    2. Cool grey-blue tint + 50% lightening
    3. Place on 1920×1080 canvas, subject on right
    4. Full-bleed ribbon overlay
    5. Save RGBA PNG
    """
    img = Image.open(image_path).convert('RGB')
    print(f"   API raw size: {img.size[0]}×{img.size[1]}")

    # 1. Cutout
    print("   🔪 rembg cutting out subject…")
    img = _professional_remove_bg(img)
    print("   ✅ Cutout complete")

    # 2. Cool grey-blue tint + lighten
    img = _apply_cool_blue_tint(img)

    # 3. Place on 1920×1080 canvas, subject on right
    canvas = _place_subject_right(img, 1920, 1080)

    # 4. Ribbon decoration across the canvas
    canvas = _draw_ribbon_curves(canvas)

    print(f"   Output size: {canvas.size[0]}×{canvas.size[1]} (RGBA, transparent background)")
    canvas.save(image_path, 'PNG')
    return image_path


# ═══════════════════════════════════════════════════════════════════════
# Main entry point
# ═══════════════════════════════════════════════════════════════════════

def generate_cover_image(title: str, output_path: str | None = None) -> str:
    """Generate a cover image for the given title via the Tencent Hunyuan 2.0 API.

    Uses SubmitHunyuanImageJob (Hunyuan 2.0) for asynchronous generation.

    Returns: path to a 1920×1080 RGBA PNG with transparent background plus
    cool grey-blue tinting and ribbon overlay.

    Requires:
        TENCENT_SECRET_ID and TENCENT_SECRET_KEY environment variables.
        rembg, Pillow, numpy, tencentcloud-sdk-python installed.

    Note: This function is OFF by default in the skill's security posture.
    Call only when the operator's confidentiality context allows transmitting
    the slide title to a third-party image-generation API.
    """
    secret_id = os.environ.get('TENCENT_SECRET_ID')
    secret_key = os.environ.get('TENCENT_SECRET_KEY')
    if not secret_id or not secret_key:
        raise EnvironmentError(
            "Missing credentials. Set TENCENT_SECRET_ID and TENCENT_SECRET_KEY "
            "environment variables before calling generate_cover_image()."
        )

    prompt = _build_prompt(title)
    print(f"🎨 Generating cover image (Hunyuan 2.0)…\n   Prompt: {prompt}")

    cred = credential.Credential(secret_id, secret_key)
    hp = HttpProfile()
    hp.endpoint = "hunyuan.tencentcloudapi.com"
    cp = ClientProfile()
    cp.httpProfile = hp
    client = hunyuan_client.HunyuanClient(cred, "ap-guangzhou", cp)

    # ── Step 1: submit async image-generation job ───────────
    req = models.SubmitHunyuanImageJobRequest()
    req.from_json_string(json.dumps({
        "Prompt": prompt,
        "NegativePrompt": "text, watermark, multiple objects, cluttered, "
                         "black background, people, anime style",
        "Resolution": "1024:1024",
        "LogoAdd": 0,
        "Num": 1,
        "Revise": 0,
    }))

    resp = client.SubmitHunyuanImageJob(req)
    job_id = resp.JobId
    print(f"   📋 Job submitted: {job_id}")

    # ── Step 2: poll for completion ─────────────────────────
    max_wait = 120   # max wait: 2 minutes
    poll_interval = 3
    elapsed = 0
    result_urls = None

    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval

        query_req = models.QueryHunyuanImageJobRequest()
        query_req.from_json_string(json.dumps({"JobId": job_id}))
        query_resp = client.QueryHunyuanImageJob(query_req)

        status = query_resp.JobStatusCode
        if status == "5":   # processing complete
            result_urls = query_resp.ResultImage
            print(f"   ✅ Job completed ({elapsed}s)")
            break
        elif status == "4":  # processing failed
            raise RuntimeError(f"Hunyuan 2.0 generation failed: {query_resp.JobStatusMsg}")
        else:
            print(f"   ⏳ Waiting… ({elapsed}s, status={status})")

    if not result_urls:
        raise RuntimeError(f"Hunyuan 2.0 generation timed out after {max_wait}s")

    # ── Step 3: download image ──────────────────────────────
    img_url = result_urls[0]
    print(f"   📥 Downloading image…")

    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix='_cover.png', prefix='mbb_')
        os.close(fd)
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    urllib.request.urlretrieve(img_url, output_path)

    # ── Step 4: post-process ────────────────────────────────
    _post_process(output_path)

    print(f"✅ Cover image saved: {output_path} ({os.path.getsize(output_path):,} bytes)")
    return output_path
