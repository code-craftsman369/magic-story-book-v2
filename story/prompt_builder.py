"""
story/prompt_builder.py
=======================
Stability AI を使った画像生成モジュール
"""

import requests
import base64


def _get_stability_key() -> str:
    try:
        import streamlit as st
        return st.secrets.get("STABILITY_API_KEY", "")
    except Exception:
        import os
        return os.environ.get("STABILITY_API_KEY", "")


def generate_image(prompt: str) -> bytes | None:
    """
    Stability AI SDXL で画像を生成してバイト列を返す。
    失敗した場合は None を返す。
    """
    api_key = _get_stability_key()
    if not api_key:
        return None

    try:
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "text_prompts": [
                    {"text": prompt, "weight": 1.0},
                    {"text": "ugly, blurry, bad anatomy, text, watermark, nsfw, violence", "weight": -1.0}
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
                "style_preset": "anime",
            },
            timeout=120,
        )

        if response.status_code == 200:
            img_b64 = response.json()["artifacts"][0]["base64"]
            return base64.b64decode(img_b64)
        return None

    except Exception:
        return None


def image_to_b64(img_bytes: bytes) -> str:
    """バイト列を Base64 文字列に変換"""
    return base64.b64encode(img_bytes).decode()
