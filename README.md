# ✨ Magic Story Book v2

**AI-Powered Personalized Picture Book Generation System**

> A scalable, agent-style AI product — not just an experiment app.

Live Demo (v1): https://magic-story-book-code-craftsman369.streamlit.app/

---

## 🎯 Design Philosophy

v1 was a proof-of-concept. v2 is designed as a **production-ready, extensible AI system**.

Key principles:

- **Separation of concerns** — UI, story logic, image generation, and output are fully decoupled
- **Pipeline architecture** — Story generation is staged (outline → body → image prompts), not monolithic
- **Character consistency** — A shared character context ensures visual coherence across all illustrations
- **Output agnostic** — The same story data can be rendered as web UI, PDF, HTML, or ZIP

---

## 🏗️ Architecture

```
magic_story_v2/
├── app.py                    # Entry point / router
├── ui/
│   └── form.py               # Structured input form (title, age, tone, pages...)
├── story/
│   ├── pipeline.py           # 3-stage generation: outline → body → image prompts
│   └── prompt_builder.py     # Character context + per-scene illustration prompts
├── output/
│   ├── pdf_builder.py        # PDF export
│   └── zip_builder.py        # Text + image ZIP export
├── utils/
│   └── helpers.py            # Shared utilities
└── output/                   # Generated files
```

---

## 🔄 Generation Pipeline

```
User Input
    ↓
[Stage 1] Story Outline
    → Page-by-page summary (JSON)
    ↓
[Stage 2] Story Body
    → Full text per page (Japanese + English)
    ↓
[Stage 3] Illustration Prompts
    → Character context + scene description per page
    ↓
[Stage 4] Image Generation
    → Stability AI SDXL (1024x1024)
    ↓
Output (Web / PDF / HTML / ZIP)
```

---

## 📋 Input Form (v2)

| Field | Type | Example |
|-------|------|---------|
| Title | Text | "こころとまほうのもり" |
| Protagonist name | Text | "こころ" |
| Target age | Select | 4–6 years |
| Story tone | Select | Gentle / Adventure / Educational |
| Theme / Keywords | Text | "friendship, forest, magic" |
| Number of pages | Slider | 3–8 pages |

---

## 📦 Output Formats

- **Web UI** — Streamlit page-by-page reader
- **PDF** — Illustrated picture book download
- **HTML** — Self-contained shareable file
- **ZIP** — Text + images for offline use

---

## 🔮 Future Roadmap

- [ ] Voice narration (text-to-speech)
- [ ] Multi-language support (EN / JA / ZH / ES)
- [ ] Character memory across sessions
- [ ] SaaS subscription model
- [ ] Parent dashboard with story history

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Anthropic Claude API (claude-opus-4-6)
- Stability AI SDXL
- ReportLab (PDF generation)

---

## 👨‍💻 Developer

**code-craftsman369** — Freelance Blockchain & AI Engineer  
GitHub: https://github.com/code-craftsman369  
Upwork: AI-Powered App Development Portfolio
