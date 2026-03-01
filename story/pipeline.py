"""
story/pipeline.py
=================
3段階ストーリー生成パイプライン

Stage 1: 物語全体の構成（各ページの概要）を生成
Stage 2: 各ページの本文を生成
Stage 3: 各ページのイラスト用プロンプトを生成
"""

import json
import anthropic


def _get_client() -> anthropic.Anthropic:
    """Anthropic クライアントを返す（st.secrets 対応）"""
    try:
        import streamlit as st
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=api_key)


# ──────────────────────────────────────────
#  Stage 1: 物語の構成を生成
# ──────────────────────────────────────────
def generate_outline(config: dict) -> list[dict]:
    """
    物語全体の構成（各ページの概要）を生成する。

    Returns:
        [
            {"page": 1, "summary": "..."},
            {"page": 2, "summary": "..."},
            ...
        ]
    """
    client = _get_client()
    pronoun = "ちゃん" if config["gender"] == "girl" else "くん"
    gender_ja = "女の子" if config["gender"] == "girl" else "男の子"

    prompt = f"""あなたは子ども向け絵本の構成作家です。
以下の設定で{config['page_count']}ページの絵本の構成を作ってください。

【設定】
タイトル: {config['title']}
主人公: {config['protagonist']}{pronoun}（{gender_ja}、{config['age_group']}対象）
相棒: {config['animal']}
トーン: {config['tone']}
キーワード: {config['keywords']}

【ルール】
・{config['page_count']}ページ構成
・各ページの概要を1〜2文で
・起承転結を意識した構成
・最後はハッピーエンド

【出力形式】必ずJSON配列のみを出力。他のテキスト不要。
[
  {{"page": 1, "summary": "ページ1の概要"}},
  {{"page": 2, "summary": "ページ2の概要"}}
]"""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()

    # JSON部分を抽出
    start = raw.find("[")
    end   = raw.rfind("]") + 1
    return json.loads(raw[start:end])


# ──────────────────────────────────────────
#  Stage 2: 各ページの本文を生成
# ──────────────────────────────────────────
def generate_pages(config: dict, outline: list[dict]) -> list[dict]:
    """
    各ページの本文（日本語・英語）を生成する。

    Returns:
        [
            {
                "page": 1,
                "summary": "...",
                "text_ja": "...",
                "text_en": "..."
            },
            ...
        ]
    """
    client = _get_client()
    pronoun = "ちゃん" if config["gender"] == "girl" else "くん"

    # 対象年齢に応じた文字数
    char_limits = {
        "3〜4歳": "40〜60文字",
        "5〜6歳": "60〜80文字",
        "7〜8歳": "80〜100文字",
        "9〜10歳": "100〜120文字",
    }
    char_limit = char_limits.get(config["age_group"], "60〜80文字")

    outline_text = "\n".join(
        [f"ページ{p['page']}: {p['summary']}" for p in outline]
    )

    prompt = f"""あなたは子ども向け絵本作家です。
以下の構成に基づいて、各ページの本文を書いてください。

【主人公】{config['protagonist']}{pronoun}、相棒: {config['animal']}
【トーン】{config['tone']}
【対象年齢】{config['age_group']}（1ページあたり{char_limit}）

【構成】
{outline_text}

【ルール】
・{config['age_group']}が読める言葉を使う
・難しい漢字はひらがなにする
・各ページは独立して読める
・英語は50〜70 words
・自然な日本語を使うこと。「関連する」「該当する」などの硬い表現や不自然な言葉は絶対に使わない
・英語テキストと日本語テキストの内容は必ず一致させること
・子どもが声に出して読んだときに自然に聞こえる文章にすること

【出力形式】必ずJSON配列のみ出力。
[
  {{"page": 1, "text_ja": "日本語本文", "text_en": "English text"}},
  {{"page": 2, "text_ja": "日本語本文", "text_en": "English text"}}
]"""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()
    start = raw.find("[")
    end   = raw.rfind("]") + 1
    pages_data = json.loads(raw[start:end])

    # outline の summary をマージ
    outline_map = {p["page"]: p["summary"] for p in outline}
    for p in pages_data:
        p["summary"] = outline_map.get(p["page"], "")

    return pages_data


# ──────────────────────────────────────────
#  Stage 3: イラストプロンプトを生成
# ──────────────────────────────────────────
def generate_image_prompts(config: dict, pages: list[dict]) -> list[dict]:
    """
    各ページのイラスト生成用プロンプトを追加する。
    キャラクター設定を共通コンテキストとして全ページに一貫性を持たせる。

    Returns:
        pages に "img_prompt" キーを追加したリスト
    """
    client = _get_client()

    # 共通キャラクターコンテキスト（全ページで使い回す）
    gender_en  = "girl" if config["gender"] == "girl" else "boy"
    style_map  = {
        "水彩画風・やわらかい": "soft watercolor illustration, pastel colors",
        "ジブリ風・あたたかい": "Studio Ghibli style, warm watercolor",
        "パステル調・かわいい": "pastel illustration, cute kawaii style",
        "絵本風・はっきり":     "children's picture book illustration, clear outlines",
    }
    art_style  = style_map.get(config["art_style"], "watercolor illustration")
    gender_style = "soft pink and lavender" if gender_en == "girl" else "cool blue and gold"

    # キャラクター共通設定
    character_context = (
        f"cute anime {gender_en} child named {config['protagonist']}, "
        f"with {config['animal']} as companion animal, "
        f"{art_style}, {gender_style} color palette, "
        f"magical sparkles, children's book art, "
        f"consistent character design throughout"
    )

    pages_summary = "\n".join(
        [f"Page {p['page']}: {p['summary']}" for p in pages]
    )

    prompt = f"""You are an expert at writing image generation prompts for children's book illustrations.

Character context (use in ALL pages for consistency):
{character_context}

Story pages:
{pages_summary}

For each page, write a Stable Diffusion prompt that:
1. Starts with the character context above
2. Adds the specific scene for that page
3. Keeps visual consistency across all pages
4. Max 80 words per prompt

Output JSON array only:
[
  {{"page": 1, "img_prompt": "..."}},
  {{"page": 2, "img_prompt": "..."}}
]"""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()
    start = raw.find("[")
    end   = raw.rfind("]") + 1
    prompt_data = json.loads(raw[start:end])

    # pages に img_prompt をマージ
    prompt_map = {p["page"]: p["img_prompt"] for p in prompt_data}
    for p in pages:
        p["img_prompt"] = prompt_map.get(p["page"], character_context)

    return pages


# ──────────────────────────────────────────
#  メインパイプライン（3段階まとめて実行）
# ──────────────────────────────────────────
def run_pipeline(config: dict, progress_callback=None) -> list[dict]:
    """
    3段階パイプラインを順番に実行する。

    Args:
        config: ui/form.py から返された設定辞書
        progress_callback: 進捗を通知するコールバック関数
                           callback(stage: int, message: str)

    Returns:
        完成したページデータのリスト
    """
    if progress_callback:
        progress_callback(1, "📖 物語の構成を考えています...")
    outline = generate_outline(config)

    if progress_callback:
        progress_callback(2, "✍️ 各ページの本文を書いています...")
    pages = generate_pages(config, outline)

    if progress_callback:
        progress_callback(3, "🎨 イラストのプロンプトを作っています...")
    pages = generate_image_prompts(config, pages)

    return pages
