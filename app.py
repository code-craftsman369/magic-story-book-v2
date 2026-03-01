"""
✨ Magic Story Book v2
======================
AI-Powered Personalized Picture Book Generation System

起動方法:
    streamlit run app.py
"""

import streamlit as st
from ui.form import render_form
from story.pipeline import run_pipeline
from story.prompt_builder import generate_image, image_to_b64
from output.pdf_builder import build_pdf

# ─────────────────────────────────────────────
#  ページ設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="✨ Magic Story Book v2",
    page_icon="📖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;700&family=Cinzel+Decorative:wght@400;700&family=Noto+Serif+JP:wght@300;400;700&display=swap');

@keyframes shimmer {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}

header, footer, #MainMenu { display: none !important; }
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"] { display: none !important; }

.stApp {
    background: linear-gradient(135deg, #1a0533 0%, #2d1b69 40%, #0d1b4b 100%);
    font-family: 'Noto Serif JP', serif;
}
.block-container {
    padding-top: 1.5rem !important;
    max-width: 860px !important;
}
.main-card {
    background: rgba(255,248,240,0.05);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin: 0.8rem 0;
}
.section-header {
    font-family: 'Shippori Mincho', serif;
    font-size: 1.1rem;
    color: #D4AF37;
    text-align: center;
    margin: 0.8rem 0 1.2rem;
    letter-spacing: 0.1em;
}
.story-ja {
    border-left: 3px solid #D4AF37;
    border-radius: 0 12px 12px 0;
    padding: 1.2rem 1.8rem;
    margin: 0.8rem 0;
    color: #F0E6FF;
    font-size: 1.05rem;
    line-height: 2.2;
    background: rgba(255,255,255,0.03);
}
.story-en {
    border-left: 3px solid #FFB7C5;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.8rem;
    margin: 0.5rem 0 1.2rem;
    color: rgba(240,230,255,0.7);
    font-size: 0.87rem;
    line-height: 1.9;
    font-style: italic;
}
.page-indicator {
    text-align: center;
    color: rgba(212,175,55,0.45);
    font-family: 'Cinzel Decorative', serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    margin: 0.8rem 0;
}
label { color: rgba(201,184,232,0.9) !important; }
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.92) !important;
    border-radius: 10px !important;
    color: #1a0533 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #D4AF37, #E8859A) !important;
    color: #1a0533 !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Shippori Mincho', serif !important;
    font-size: 1.0rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(212,175,55,0.35) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  セッションステート初期化
# ─────────────────────────────────────────────
for k, v in {
    "v2_page":    "form",
    "v2_config":  None,
    "v2_pages":   [],
    "v2_img_b64": {},
    "v2_current": 1,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


def do_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


# ─────────────────────────────────────────────
#  画面1: 入力フォーム
# ─────────────────────────────────────────────
if st.session_state.v2_page == "form":
    config = render_form()
    if config:
        st.session_state.v2_config = config
        st.session_state.v2_page   = "generating"
        do_rerun()


# ─────────────────────────────────────────────
#  画面2: 生成中（進捗表示）
# ─────────────────────────────────────────────
elif st.session_state.v2_page == "generating":
    st.markdown("""
    <div style="text-align:center; padding:2rem 0;">
        <div style="font-family:'Cinzel Decorative',serif; font-size:1.8rem;
                    background:linear-gradient(135deg,#FFD700,#FFB7C5,#C9B8E8,#FFD700);
                    background-size:300% 300%; animation:shimmer 4s ease infinite;
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            ✨ Magic Story Book v2 ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    config       = st.session_state.v2_config
    progress_bar = st.progress(0)
    status_text  = st.empty()

    def on_progress(stage, message):
        progress_bar.progress(stage / 6)
        status_text.markdown(
            f'<div style="text-align:center;color:#D4AF37;'
            f'font-family:\'Shippori Mincho\',serif;">{message}</div>',
            unsafe_allow_html=True
        )

    pages = run_pipeline(config, progress_callback=on_progress)
    st.session_state.v2_pages = pages

    img_b64 = {}
    total   = len(pages)
    for i, p in enumerate(pages):
        progress_bar.progress((3 + i + 1) / (3 + total + 1))
        status_text.markdown(
            f'<div style="text-align:center;color:#D4AF37;'
            f'font-family:\'Shippori Mincho\',serif;">'
            f'🎨 ページ{p["page"]}のイラストをかいているよ... ({i+1}/{total})</div>',
            unsafe_allow_html=True
        )
        img_bytes = generate_image(p["img_prompt"])
        if img_bytes:
            img_b64[p["page"]] = image_to_b64(img_bytes)

    st.session_state.v2_img_b64 = img_b64
    st.session_state.v2_current = 1
    st.session_state.v2_page    = "reading"
    progress_bar.progress(1.0)
    do_rerun()


# ─────────────────────────────────────────────
#  画面3: 絵本を読む
# ─────────────────────────────────────────────
elif st.session_state.v2_page == "reading":
    pages   = st.session_state.v2_pages
    current = st.session_state.v2_current
    config  = st.session_state.v2_config
    total   = len(pages)

    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0 0.3rem;">
        <div style="font-family:'Cinzel Decorative',serif; font-size:1.6rem; font-weight:700;
                    background:linear-gradient(135deg,#FFD700,#FFB7C5,#C9B8E8,#FFD700);
                    background-size:300% 300%; animation:shimmer 4s ease infinite;
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            ✨ {config['title']} ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="page-indicator">— Page {current} of {total} —</div>',
        unsafe_allow_html=True
    )

    page_data = next((p for p in pages if p["page"] == current), None)
    if page_data:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)

        img_b64 = st.session_state.v2_img_b64.get(current)
        if img_b64:
            st.markdown(f"""
            <img src="data:image/png;base64,{img_b64}"
                 style="width:100%;border-radius:16px;
                        border:1px solid rgba(212,175,55,0.4);
                        margin-bottom:1rem;" />
            """, unsafe_allow_html=True)

        lang = config.get("language", "日本語 + 英語")
        if "日本語" in lang:
            st.markdown(
                f'<div class="story-ja">{page_data["text_ja"]}</div>',
                unsafe_allow_html=True
            )
        if "英語" in lang:
            st.markdown(
                f'<div class="story-en">{page_data["text_en"]}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # PDFダウンロードボタン
    if st.session_state.v2_pages:
        pdf_bytes = build_pdf(
            config,
            st.session_state.v2_pages,
            st.session_state.v2_img_b64
        )
        st.download_button(
            label="📥 PDFとしてダウンロード",
            data=pdf_bytes,
            file_name=f"{config['title']}.pdf",
            mime="application/pdf",
            key="pdf_download"
        )
    c1, c2 = st.columns(2)
    with c1:
        if current > 1:
            if st.button("← まえのページ", key="prev"):
                st.session_state.v2_current -= 1
                do_rerun()
    with c2:
        if current < total:
            if st.button("つぎのページへ →", key="next"):
                st.session_state.v2_current += 1
                do_rerun()
        else:
            if st.button("✨ さいごのページへ", key="ending"):
                st.session_state.v2_page = "ending"
                do_rerun()


# ─────────────────────────────────────────────
#  画面4: エンディング
# ─────────────────────────────────────────────
elif st.session_state.v2_page == "ending":
    config  = st.session_state.v2_config
    pronoun = "ちゃん" if config["gender"] == "girl" else "くん"
    emoji   = "🌸" if config["gender"] == "girl" else "⭐"

    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-family:'Cinzel Decorative',serif; font-size:1.6rem; font-weight:700;
                    background:linear-gradient(135deg,#FFD700,#FFB7C5,#C9B8E8,#FFD700);
                    background-size:300% 300%; animation:shimmer 4s ease infinite;
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            ✨ Magic Story Book v2 ✨
        </div>
    </div>
    <div style="text-align:center;font-size:2rem;margin:0.8rem 0;">{emoji} ⭐ {emoji}</div>
    <div class="main-card" style="text-align:center;">
        <div style="font-family:'Shippori Mincho',serif;font-size:1.1rem;
                    color:rgba(201,184,232,0.9);line-height:2.2;margin-bottom:1.5rem;">
            {config['protagonist']}{pronoun}、このものがたりは<br>
            あなたのためだけにうまれた<br>
            せかいにひとつだけのまほうのえほんです。
        </div>
        <div style="background:linear-gradient(135deg,rgba(212,175,55,0.12),rgba(255,183,197,0.08));
                    border:1px solid rgba(212,175,55,0.4);border-radius:16px;padding:1.5rem 2rem;">
            <div style="font-family:'Shippori Mincho',serif;font-size:1.3rem;
                        color:#FFD700;line-height:2.0;">
                パパより、いつもありがとう。<br>大すきだよ。💛
            </div>
            <div style="font-size:0.9rem;color:rgba(255,215,0,0.65);
                        margin-top:0.8rem;font-style:italic;">
                From Dad — Thank you always, {config['protagonist']}.<br>
                I love you more than all the stars. ⭐
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("← まえのページ", key="back"):
            st.session_state.v2_page = "reading"
            do_rerun()
    with c2:
        if st.button("🔮 あたらしいものがたりをつくる", key="restart"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            do_rerun()
