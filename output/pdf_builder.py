"""
output/pdf_builder.py
=====================
fpdf2 を使って日本語対応PDFを生成するモジュール
"""

import base64
import io
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image as PILImage


def _font_path() -> str:
    """フォントファイルのパスを返す"""
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "NotoSansCJKjp-Regular.otf"),
        "NotoSansCJKjp-Regular.otf",
    ]
    for p in candidates:
        p = os.path.abspath(p)
        if os.path.exists(p):
            return p
    return ""


def build_pdf(config: dict, pages: list, img_b64: dict) -> bytes:
    """
    絵本データからPDFを生成してバイト列を返す。
    """
    font_file = _font_path()
    lang      = config.get("language", "日本語 + 英語")
    pronoun   = "ちゃん" if config["gender"] == "girl" else "くん"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    # フォント登録
    if font_file:
        pdf.add_font("Noto", "", font_file)
        font = "Noto"
    else:
        font = "Helvetica"

    # ─── 表紙 ────────────────────────────────
    pdf.add_page()
    _bg(pdf, "#1a0533")
    _border(pdf)

    pdf.set_font(font, size=24)
    pdf.set_text_color(255, 215, 0)
    pdf.set_y(80)
    pdf.cell(0, 12, f"✨ {config['title']} ✨",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=13)
    pdf.set_text_color(201, 184, 232)
    pdf.set_y(102)
    pdf.cell(0, 8, f"{config['protagonist']}{pronoun}のためのまほうのえほん",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=28)
    pdf.set_text_color(212, 175, 55)
    pdf.set_y(125)
    pdf.cell(0, 14, "✨ ⭐ ✨",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=10)
    pdf.set_text_color(212, 175, 55)
    pdf.set_y(270)
    pdf.cell(0, 6, "Magic Story Book v2",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ─── 各ページ ─────────────────────────────
    for page_data in pages:
        n = page_data["page"]
        pdf.add_page()
        _bg(pdf, "#1a0533")

        # ページ番号
        pdf.set_font(font, size=9)
        pdf.set_text_color(212, 175, 55)
        pdf.set_y(6)
        pdf.cell(0, 6, f"— Page {n} of {len(pages)} —",
                 align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # イラスト（上部固定：y=14, 幅140mm・高さは縦横比に応じて自動）
        IMG_X, IMG_Y, IMG_W, IMG_MARGIN = 35, 14, 140, 5
        text_start_y = IMG_Y + 100  # 画像なし時のフォールバック

        b64 = img_b64.get(n)
        if b64:
            try:
                img_bytes = base64.b64decode(b64)
                pil_img   = PILImage.open(io.BytesIO(img_bytes))
                # 描画前に実際の高さ(mm)を縦横比から計算
                w_px, h_px = pil_img.size
                draw_h = IMG_W * (h_px / w_px)
                img_io = io.BytesIO()
                pil_img.save(img_io, format="PNG")
                img_io.seek(0)
                pdf.image(img_io, x=IMG_X, y=IMG_Y, w=IMG_W)
                # 画像下端 + マージン をテキスト開始位置に設定
                text_start_y = IMG_Y + draw_h + IMG_MARGIN
            except Exception:
                pass

        # テキストはイラストの実際の下端から開始

        # 区切り線
        pdf.set_draw_color(212, 175, 55)
        pdf.set_line_width(0.3)
        pdf.line(10, text_start_y, 200, text_start_y)

        # 日本語テキスト
        if "日本語" in lang and page_data.get("text_ja"):
            pdf.set_font(font, size=11)
            pdf.set_text_color(240, 230, 255)
            pdf.set_xy(10, text_start_y + 4)
            pdf.multi_cell(190, 7, page_data["text_ja"], align="L")

        # 英語テキスト
        if "英語" in lang and page_data.get("text_en"):
            pdf.set_font(font, size=11)
            pdf.set_text_color(190, 170, 220)
            pdf.set_xy(10, pdf.get_y() + 3)
            pdf.multi_cell(190, 6, page_data["text_en"], align="L")

    # ─── エンディング ─────────────────────────
    pdf.add_page()
    _bg(pdf, "#1a0533")
    _border(pdf)

    pdf.set_font(font, size=22)
    pdf.set_text_color(255, 215, 0)
    pdf.set_y(60)
    pdf.cell(0, 12, "🌟 おわり 🌟",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=12)
    pdf.set_text_color(201, 184, 232)
    for line in [
        f"{config['protagonist']}{pronoun}、このものがたりは",
        "あなたのためだけにうまれた",
        "せかいにひとつだけのまほうのえほんです。",
    ]:
        pdf.cell(0, 9, line, align="C",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # メッセージボックス
    pdf.set_fill_color(45, 27, 105)
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.8)
    pdf.set_xy(25, 155)
    pdf.cell(160, 52, "", border=1, fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=13)
    pdf.set_text_color(255, 215, 0)
    pdf.set_y(165)
    pdf.cell(0, 9, "パパより、いつもありがとう。",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 9, "大すきだよ。💛",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font(font, size=9)
    pdf.set_text_color(201, 184, 232)
    pdf.set_y(192)
    pdf.cell(0, 6, "From Dad — I love you more than all the stars.",
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())


def _bg(pdf: FPDF, hex_color: str):
    """背景色を塗る"""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, 210, 297, style="F")


def _border(pdf: FPDF):
    """装飾ボーダーを描く"""
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, 190, 277)
    pdf.set_line_width(0.4)
    pdf.rect(12, 12, 186, 273)
