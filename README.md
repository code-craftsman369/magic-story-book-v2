# ✨ Magic Story Book v2

**AI-Powered Personalized Bilingual Picture Books — Made by a Dad, Built for Every Child**

> *I wanted to give my kids something no store could sell: a story made just for them.*  
> That idea became a system. This is Magic Story Book v2.

🌐 Live Demo (v1): https://magic-story-book-code-craftsman369.streamlit.app/

---

## 🧡 Why This Exists

My daughter is 9. My son is 7. Like most working parents, I struggled to find bedtime stories that felt truly *theirs* — with their name, their interests, their world.

I also wanted them to grow up comfortable in English, but flashcards and textbooks never stuck. What if the learning material was a story they actually cared about?

So I built it.

Magic Story Book v2 generates personalized, bilingual picture books in minutes — complete with illustrations, bilingual text (Japanese + English), and a print-ready PDF. It started as a gift for my kids. It's now designed to be a product for any parent who feels the same way.

---

## 👨‍👩‍👧‍👦 Who This Is For

- **Parents of children ages 4–10** who want something more personal than off-the-shelf books
- **Families introducing English at home** who need engaging, low-pressure bilingual material
- **Parents marking a special occasion** — birthdays, graduations, "just because" moments
- **Educators and tutors** looking for AI-generated, curriculum-adjacent story content

---

## 🎯 Problems This Solves

| Problem | What Magic Story Book Does |
|---|---|
| Running out of read-aloud ideas | Generates a fresh, custom story in minutes |
| English learning that doesn't stick | Stories in both Japanese and English — same content, natural exposure |
| Creating original teaching materials takes hours | Structured AI pipeline handles outline, body, and illustrations automatically |
| Generic books don't feel personal | Every story uses the child's name, age, and chosen theme |

---

## ⚡ Core Value Proposition

**In under 5 minutes, any parent can create:**

- 📖 A 3–8 page illustrated picture book
- 🌏 Fully bilingual (Japanese + English on every page)
- 🎨 AI-generated illustrations matched to the story
- 📄 A print-ready PDF — ready to read on screen or send to a print shop
- 💛 A story their child will recognize as made just for them

---

## 🔄 How It Works

The generation pipeline runs in four structured stages — ensuring story coherence, character consistency, and output quality:

```
User Input (name, age, theme, tone, pages)
    ↓
[Stage 1] Story Outline
    → Page-by-page narrative arc (JSON)
    ↓
[Stage 2] Story Body
    → Full bilingual text per page (Japanese + English)
    ↓
[Stage 3] Illustration Prompts
    → Character context + scene description (consistent across all pages)
    ↓
[Stage 4] Image Generation
    → Stability AI SDXL (1024×1024)
    ↓
Output — Web reader / PDF / HTML / ZIP
```

This staged approach — rather than a single monolithic prompt — is what enables narrative coherence, visual consistency, and extensibility across output formats.

---

## 📋 Story Configuration

| Field | Options | Example |
|---|---|---|
| Title | Free text | "こころとまほうのもり" |
| Protagonist name | Free text | "こころ" |
| Gender | Boy / Girl | Girl |
| Target age | 4–10 years | 6 years |
| Story tone | Gentle / Adventure / Educational | Gentle |
| Theme / Keywords | Free text | "friendship, forest, magic" |
| Number of pages | 3–8 | 3 pages |
| Language output | JA / EN / Bilingual | Japanese + English |

---

## 📦 Output Formats

- **Web UI** — Streamlit page-by-page reader, shareable via link
- **PDF** — Illustrated picture book, print-ready download
- **HTML** — Self-contained file, no server required
- **ZIP** — Raw text + images for offline use or custom rendering

---

## 🏗️ Technical Architecture

Designed with separation of concerns from day one — each layer is independently replaceable:

```
magic_story_v2/
├── app.py                   # Entry point / router
├── ui/
│   └── form.py              # Structured input form
├── story/
│   ├── pipeline.py          # 3-stage generation orchestrator
│   └── prompt_builder.py    # Character context + illustration prompts
├── output/
│   ├── pdf_builder.py       # fpdf2-based PDF export
│   └── zip_builder.py       # Text + image ZIP export
└── utils/
    └── helpers.py           # Shared utilities
```

**Key design decisions:**
- **Pipeline over monolith** — Staged generation allows partial regeneration and easier debugging
- **Character context injection** — A shared character descriptor is prepended to every illustration prompt, ensuring visual consistency across pages
- **Output-agnostic story data** — The same JSON story object drives web UI, PDF, HTML, and ZIP with no duplication
- **Dynamic layout** — PDF image heights are calculated from actual pixel dimensions, eliminating text/illustration overlap

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Anthropic Claude API (`claude-opus-4-6`)
- Stability AI SDXL
- fpdf2 (PDF generation)
- Pillow (image processing)

---

## 🔮 Roadmap

- [ ] **Voice narration** — Text-to-speech per page (Japanese + English)
- [ ] **Multi-language support** — Chinese, Spanish, Korean
- [ ] **Character memory** — Persistent protagonists across multiple books
- [ ] **Parent dashboard** — Story history, reprint, share
- [ ] **Education SaaS** — Subscription model for schools and tutoring centers
- [ ] **API access** — Embed story generation into third-party apps

---

## 👨‍💻 Developer

**code-craftsman369** — Freelance AI & Blockchain Engineer

This project is part of an active portfolio of AI-powered applications built for real use cases — not just demos.

- GitHub: https://github.com/code-craftsman369
- X: [@web3_builder369](https://x.com/web3_builder369)
- Upwork: AI-Powered App Development Portfolio

---

*Built with care — for two kids in Japan, and every child after them.*
