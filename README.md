# 📖 Bible RAG Agent

A Retrieval-Augmented Generation (RAG) chatbot that answers **Hebrew** questions about the Hebrew Bible using a local Chroma vector database and the OpenAI API.

The system retrieves relevant Bible passages before generating an answer and cites the relevant verses.

---

# ✨ Features

* 🇮🇱 Hebrew-only chat
* 📄 PDF-based knowledge source
* 🧠 OpenAI for embeddings and answer generation
* 🔎 Local Chroma vector database
* 📚 Verse-aware chunking
* 💬 In-memory conversation history
* 🔄 Follow-up question refinement
* 📍 Source references in every answer

---

# 🚀 Getting Started

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure

Create a `.env` file (see the example below).

Example:

```env
OPENAI_API_KEY=your_api_key

OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

BIBLE_PDF_PATH=./data/input/hebrew_bible.pdf
CHROMA_PERSIST_DIR=./data/chroma

CHUNK_WINDOW_SIZE=8
CHUNK_OVERLAP=2
RETRIEVER_TOP_K=5
CONVERSATION_MAX_TURNS=6
```

## 3. Add the Bible PDF

```text
data/input/hebrew_bible.pdf
```

## 4. Build the vector database

```bash
python src/indexing/build_index.py
```

## 5. Start the chatbot

```bash
python src/main.py
```

---

# ⚙️ System Flow

### 📦 Indexing

```text
PDF → Extract → Clean → Parse → Chunk → Embed → Chroma
```

### 💬 Chat

```text
User → CLI → Question Refiner → Retriever → Prompt Builder → OpenAI → Validator → Answer
```

---

# 🏗️ Design Principles

* Keep it simple (KISS)
* Small, focused modules
* Strict separation of concerns
* Hebrew-first user experience
* Configurable through `.env`

---

# 🔍 Engineering Challenges

* Reliable extraction of Hebrew text containing nikud and te'amim
* Parsing Hebrew chapter and verse numbering
* Preserving verse boundaries during text normalization
* Resolving ambiguous follow-up questions using conversation history
* Building a modular RAG pipeline with clear separation of responsibilities
* Keeping the user experience entirely in Hebrew while maintaining an English codebase

---

# ⚠️ Known Limitations

* Answer quality depends on the chosen model — smaller/cheaper models (e.g. `gpt-4o-mini`, `gpt-4.1-mini`) can give weaker or less accurate answers; larger models improve results. change model type in `.env` file for better results.
* Right-to-left (RTL) rendering of Hebrew in the CLI is not fully resolved yet, so Hebrew output may display awkwardly in some terminals.

---

# 🚧 Future Ideas

* 📝 Persistent conversation history
* 👤 Multi-user sessions and session management
* 🤖 LLM-assisted indexing for difficult parsing and cleaning edge cases
* 🧗 Optimize token usage by separating models for diff tasks
* 📄 Support additional document formats (DOCX, Markdown, plain text)
* 🌐 Multiple interfaces (CLI, Web UI, REST API, Python package)
* 🔍 Hybrid retrieval (semantic + keyword search)
* ⚡ Incremental indexing instead of rebuilding the entire vector database
* 🧠 Conversation summarization for long chats
* 📊 Better retrieval diagnostics and evaluation metrics
* 🧪 Expanded automated test coverage
* 📈 Structured logging and performance metrics

---

# 🤖 AI Usage

AI tools were used for:

* Implementing parts of the code from detailed instructions
* Code reviews and refactoring suggestions
* Challenging design decisions with alternative approaches
* Brainstorming edge cases
* Improving documentation (including this README🙃)
* Parsing strategy after extracting text

The project's architecture, data pipeline, module structure, orchestration, design decisions, and overall implementation were planned, managed, and driven by me.
