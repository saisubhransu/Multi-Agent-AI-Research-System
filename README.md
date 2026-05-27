# ResearchMind 🔬

An elegant, multi-agent research pipeline that automates the process of searching, reading, writing, and reviewing research reports on any topic. Powered by **LangChain** and **Groq**.

## Features

- **Search Agent**: Searches the web using the Tavily API for fresh, reliable facts.
- **Reader Agent**: Scrapes and parses top resource URLs for deeper reading.
- **Writer Chain**: Synthesizes the information into a structured, professional report.
- **Critic Chain**: Reviews the final report and provides a critique and score.
- **Interactive UI**: A modern, responsive Streamlit dashboard tracking the execution in real time.

---

## Project Structure

```text
├── .env.example       # Template for API keys
├── .gitignore         # Ignores secrets and environments
├── agents.py          # LLM definitions & agent creation
├── app.py             # Streamlit application UI
├── pipeline.py        # Pipeline workflow coordinator
├── requirements.txt   # Project dependencies
└── tools.py           # Tavily search & BeautifulSoup scraper tools
```

---

## Setup & Running

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd MultiAgents
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Install packages:
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Fill in your API keys in `.env`:
     - `TAVILY_API_KEY` (from [Tavily](https://tavily.com))
     - `OPENAI_API_KEY` (input your [Groq](https://console.groq.com) API key starting with `gsk_`)

4. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```
