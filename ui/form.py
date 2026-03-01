"""
ui/form.py
==========
入力フォームモジュール
ユーザーから絵本の設定を受け取り、辞書形式で返す
"""

import streamlit as st


def render_form() -> dict | None:
    """
    絵本生成用の入力フォームを表示する。
    「物語をつくる！」ボタンが押されたら入力値を辞書で返す。
    未入力がある場合は None を返す。
    """

    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <div style="font-family:'Cinzel Decorative',serif; font-size:1.8rem; font-weight:700;
                    background:linear-gradient(135deg,#FFD700,#FFB7C5,#C9B8E8,#FFD700);
                    background-size:300% 300%; animation:shimmer 4s ease infinite;
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            ✨ Magic Story Book v2 ✨
        </div>
        <div style="color:rgba(201,184,232,0.8); font-size:0.9rem; letter-spacing:0.15em;
                    margin-top:0.3rem;">
            〜 あなただけの絵本をつくろう 〜
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📖 絵本の設定</div>', unsafe_allow_html=True)

    # ── 基本設定 ──
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input(
            "📚 絵本のタイトル",
            placeholder="例：こころとまほうのもり",
            key="v2_title"
        )
    with col2:
        protagonist = st.text_input(
            "✨ 主人公の名前",
            placeholder="例：こころ",
            key="v2_protagonist"
        )

    col3, col4 = st.columns(2)
    with col3:
        gender = st.radio(
            "👦👧 主人公は？",
            options=["👧 女の子", "👦 男の子"],
            horizontal=True,
            key="v2_gender"
        )
    with col4:
        age_group = st.selectbox(
            "🎂 対象年齢",
            options=["3〜4歳", "5〜6歳", "7〜8歳", "9〜10歳"],
            key="v2_age"
        )

    # ── 物語の設定 ──
    st.markdown("---")
    st.markdown('<div class="section-header">🎭 物語の設定</div>', unsafe_allow_html=True)

    tone = st.select_slider(
        "🌈 物語のトーン",
        options=["やさしい・ほんわか", "ふしぎ・まほう", "ぼうけん・わくわく", "がくしゅう・発見"],
        key="v2_tone"
    )

    keywords = st.text_input(
        "🔑 テーマ・キーワード",
        placeholder="例：友情、森、動物、食べ物（カンマ区切り）",
        key="v2_keywords"
    )

    animal = st.text_input(
        "🦊 相棒の動物",
        placeholder="例：うさぎ、ねこ、くま",
        key="v2_animal"
    )

    # ── 絵本の構成 ──
    st.markdown("---")
    st.markdown('<div class="section-header">📄 絵本の構成</div>', unsafe_allow_html=True)

    page_count = st.slider(
        "📖 ページ数",
        min_value=3,
        max_value=8,
        value=5,
        step=1,
        key="v2_page_count"
    )

    col5, col6 = st.columns(2)
    with col5:
        art_style = st.selectbox(
            "🎨 絵のスタイル",
            options=[
                "水彩画風・やわらかい",
                "ジブリ風・あたたかい",
                "パステル調・かわいい",
                "絵本風・はっきり",
            ],
            key="v2_art_style"
        )
    with col6:
        language = st.selectbox(
            "🌍 言語",
            options=["日本語 + 英語", "日本語のみ", "英語のみ"],
            key="v2_language"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── 生成ボタン ──
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 魔法の絵本をつくる！", key="v2_generate"):
        # バリデーション
        missing = []
        if not title:
            missing.append("絵本のタイトル")
        if not protagonist:
            missing.append("主人公の名前")
        if not keywords:
            missing.append("テーマ・キーワード")
        if not animal:
            missing.append("相棒の動物")

        if missing:
            st.warning(f"以下を入力してください：{' / '.join(missing)}")
            return None

        return {
            "title":       title,
            "protagonist": protagonist,
            "gender":      "girl" if "女" in gender else "boy",
            "age_group":   age_group,
            "tone":        tone,
            "keywords":    keywords,
            "animal":      animal,
            "page_count":  page_count,
            "art_style":   art_style,
            "language":    language,
        }

    return None
