# 🔍 Code Reviewer CLI

An AI-powered code reviewer that runs directly in your terminal — built with **Gemini AI** and **Model Context Protocol (MCP)**. Works globally from any project folder on your machine.

---

## ✨ What it does

Instead of copy-pasting code into ChatGPT or Gemini's browser UI, just run one command from any project folder:

```bash
code-reviewer
```

It shows you a numbered list of your code files, you pick one, and Gemini reviews it right there in your terminal — structured, clear, and instant.

```
╭─────────────────────────────────────╮
│ Welcome to Code Reviewer! 🤖        │
│ Powered by Gemini + MCP             │
╰─────────────────────────────────────╯

📁 Files available for review:

  [1] main.py
  [2] utils.py
  [3] database.py
  [4] AiService.java
  [5] UserController.java

Enter file number: 3

✅ Selected: database.py
⠦ Reviewing your code...

╭─────────────────────────────────────────╮
│ 📋 Code Review — database.py            │
│                                         │
│ 🐛 BUGS FOUND                           │
│   - Line 42: connection never closed... │
│                                         │
│ ⚠️  CODE QUALITY                        │
│   - Function too long, split it up...   │
│                                         │
│ ✅ GOOD PRACTICES                       │
│   - Good use of try/except blocks...    │
│                                         │
│ 💡 SUGGESTIONS                          │
│   - Add connection pooling...           │
╰─────────────────────────────────────────╯
```

---

## 🏗️ Project Structure

```
code-reviewer/
├── server.py        ← MCP Server (exposes read_file tool to Gemini)
├── client.py        ← Connects Gemini API to the MCP server
├── cli.py           ← CLI interface — file picker + terminal output
├── pyproject.toml   ← Package config (makes it globally installable)
├── requirements.txt ← Dependencies
└── .env             ← Your API key (never commit this)
```

---

## 🧠 How it works — The Full Flow

### Big picture

```
You type: code-reviewer
              ↓
         cli.py
         Shows numbered file list
         User picks a file
              ↓
         client.py
         Starts MCP server
         Connects Gemini to tools
         Runs the agentic loop
              ↓
         server.py
         Reads the file from disk
         Returns contents
              ↓
         Gemini
         Receives file contents
         Generates structured review
              ↓
         cli.py
         Prints review beautifully ✅
```

---

### The 3-Layer Architecture

```
┌─────────────────────────────────────────┐
│  cli.py  ←  Controller Layer            │
│  Shows UI, takes input, prints output   │
├─────────────────────────────────────────┤
│  client.py  ←  Service Layer            │
│  Connects Gemini + MCP, runs the loop   │
├─────────────────────────────────────────┤
│  server.py  ←  Tool Layer               │
│  Exposes read_file tool via MCP         │
└─────────────────────────────────────────┘
```

---

### What is MCP?

**Model Context Protocol (MCP)** is an open standard by Anthropic that lets AI models interact with external tools and data sources. Instead of you manually reading a file and pasting it into a prompt, MCP lets Gemini **decide what it needs and fetch it itself**.

```
Without MCP:
  You read file → paste into prompt → AI responds

With MCP:
  You ask AI → AI calls read_file tool itself → AI responds
```

---

### The client.py Agentic Loop — 5 Steps

This is the heart of the project. `client.py` does 5 things in order:

```
Step 1 — START
  Launches server.py as a subprocess
  (like starting a background Java process)
       ↓
Step 2 — DISCOVER
  Asks MCP server: "what tools do you have?"
  Server replies:  "I have read_file"
       ↓
Step 3 — TELL
  Tells Gemini: "you have read_file tool available,
                 here's what it does and how to call it"
       ↓
Step 4 — LOOP (the agentic loop)
  Sends user's request to Gemini
  Gemini thinks: "I need to call read_file to see the code"
  client.py calls read_file on MCP server
  MCP server reads the actual file from disk
  client.py feeds file contents back to Gemini
  Gemini now has the code and generates the review
       ↓
Step 5 — RETURN
  Sends final review text back to cli.py
  cli.py prints it in a beautiful panel
```

---

### Why this matters

In a traditional setup, you hardcode what the AI gets. With MCP + an agentic loop, **the AI decides what tools to call and when** — making it genuinely autonomous. This is the foundation of how modern AI agents work.

---

## 🌍 Global Installation

This tool is packaged so it works from **any folder** on your machine — not just the project folder.

```bash
# Clone the repo
git clone https://github.com/vanipentabalaji/code-reviewer
cd code-reviewer

# Install globally
pip install -e .
```

The `-e` flag means "editable install" — installs globally but reads from your local files. Any changes you make to the code apply immediately without reinstalling.

After installation, `code-reviewer` becomes a globally available command — just like `git` or `python`:

```bash
# Works from ANY folder on your machine
cd C:\Users\you\any-project
code-reviewer
```

This works because `pyproject.toml` registers the command:
```toml
[project.scripts]
code-reviewer = "cli:main"
#     ↑              ↑    ↑
# the command    the file  the function
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Setup

```bash
# 1. Clone
git clone https://github.com/vanipentabalaji/code-reviewer
cd code-reviewer

# 2. Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install globally
pip install -e .

# 4. Add your API key
# Create a .env file in the code-reviewer folder:
GEMINI_API_KEY=your_key_here
```

### Run from anywhere

```bash
cd your-project-folder
code-reviewer
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Gemini AI](https://ai.google.dev) | AI reasoning and code review via function calling |
| [MCP](https://modelcontextprotocol.io) | Tool server protocol — lets AI call tools autonomously |
| [Rich](https://rich.readthedocs.io) | Beautiful terminal UI — panels, spinners, colors |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Loads API key from .env file |
| [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) | Packages the project as an installable CLI tool |

---

## 📂 Supported File Types

The tool automatically finds and lists these file types in your project:

`.py` `.java` `.js` `.ts` `.cpp` `.c` `.html` `.css` `.json`

It skips irrelevant folders automatically: `venv/`, `node_modules/`, `__pycache__/`, `target/`, `build/`, `.git/`

---

## 🧩 What I Learned

- How **Model Context Protocol (MCP)** works — servers, clients, tool registration
- Building an **agentic loop** where AI autonomously decides which tools to call
- Connecting **Gemini API function calling** with a custom MCP server
- Packaging a Python CLI as a **globally installable tool** using `pyproject.toml`

---

## 📌 Future Improvements

- [ ] Review multiple files at once
- [ ] Export review to a `.md` file
- [ ] Add severity levels (critical / warning / info)
- [ ] Support for reviewing git diffs (`git diff` integration)
- [ ] Web UI version

---

## 🔗 Related

- [Anthropic MCP Documentation](https://modelcontextprotocol.io)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [MCP Course by Anthropic](https://www.anthropic.com)
